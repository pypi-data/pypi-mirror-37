import io
import json
import logging
import socket
import struct
import threading
import traceback
import weakref
import paramiko
import tornado.web

from tornado.ioloop import IOLoop
from tornado.options import options
from webssh import settings
from webssh.utils import (
    is_valid_ip_address, is_valid_port, is_valid_hostname,
    to_bytes, to_str, to_int, to_ip_address, UnicodeType
)
from webssh.worker import Worker, recycle_worker, workers

try:
    from concurrent.futures import Future
except ImportError:
    from tornado.concurrent import Future

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError


DELAY = 3
KEY_MAX_SIZE = 16384
DEFAULT_PORT = 22


class InvalidValueError(Exception):
    pass


class MixinHandler(object):

    is_open_to_public = None
    forbid_public_http = None

    custom_headers = {
        'Server': 'TornadoServer'
    }

    def initialize(self):
        if self.is_open_to_public is None:
            MixinHandler.is_open_to_public = settings.is_open_to_public

        if self.forbid_public_http is None:
            MixinHandler.forbid_public_http = options.fbidhttp

        if self.is_forbidden():
            result = '{} 403 Forbidden\r\n\r\n'.format(self.request.version)
            self.request.connection.stream.write(to_bytes(result))
            self.request.connection.close()
            raise ValueError('Accesss denied')

    def is_forbidden(self):
        """
        Following requests are forbidden:
        * requests not come from trusted_downstream (if set).
        * non-https requests from a public network.
        """
        context = self.request.connection.context
        ip = context.address[0]
        lst = context.trusted_downstream

        if lst and ip not in lst:
            logging.warning(
                'IP {!r} not found in trusted downstream {!r}'.format(ip, lst)
            )
            return True

        if self.is_open_to_public and self.forbid_public_http:
            if context._orig_protocol == 'http':
                ipaddr = to_ip_address(ip)
                if not ipaddr.is_private:
                    logging.warning('Public non-https request is forbidden.')
                    return True

    def set_default_headers(self):
        for header in self.custom_headers.items():
            self.set_header(*header)

    def get_value(self, name):
        value = self.get_argument(name)
        if not value:
            raise InvalidValueError('Missing value {}'.format(name))
        return value

    def get_client_addr(self):
        return self.get_real_client_addr() or self.request.connection.context.\
                address

    def get_real_client_addr(self):
        ip = self.request.remote_ip

        if ip == self.request.headers.get('X-Real-Ip'):
            port = self.request.headers.get('X-Real-Port')
        elif ip in self.request.headers.get('X-Forwarded-For', ''):
            port = self.request.headers.get('X-Forwarded-Port')
        else:
            # not running behind an nginx server
            return

        port = to_int(port)
        if port is None or not is_valid_port(port):
            # fake port
            port = 65535

        return (ip, port)


class NotFoundHandler(MixinHandler, tornado.web.ErrorHandler):

    def initialize(self):
        super(NotFoundHandler, self).initialize()

    def prepare(self):
        raise tornado.web.HTTPError(404)


class IndexHandler(MixinHandler, tornado.web.RequestHandler):

    def initialize(self, loop, policy, host_keys_settings):
        self.loop = loop
        self.policy = policy
        self.host_keys_settings = host_keys_settings
        self.ssh_client = self.get_ssh_client()
        self.privatekey_filename = None
        self.debug = self.settings.get('debug', False)
        self.result = dict(id=None, status=None, encoding=None)
        super(IndexHandler, self).initialize()

    def write_error(self, status_code, **kwargs):
        if self.request.method != 'POST' or not settings.swallow_http_errors:
            super(IndexHandler, self).write_error(status_code, **kwargs)
        else:
            exc_info = kwargs.get('exc_info')
            if exc_info:
                reason = getattr(exc_info[1], 'log_message', None)
                if reason:
                    self._reason = reason
            self.result.update(status=self._reason)
            self.set_status(200)
            self.finish(self.result)

    def get_ssh_client(self):
        ssh = paramiko.SSHClient()
        ssh._system_host_keys = self.host_keys_settings['system_host_keys']
        ssh._host_keys = self.host_keys_settings['host_keys']
        ssh._host_keys_filename = self.host_keys_settings['host_keys_filename']
        ssh.set_missing_host_key_policy(self.policy)
        return ssh

    def get_privatekey(self):
        name = 'privatekey'
        lst = self.request.files.get(name)
        if lst:
            # multipart form
            self.privatekey_filename = lst[0]['filename']
            data = lst[0]['body']
            value = self.decode_argument(data, name=name).strip()
        else:
            # urlencoded form
            value = self.get_argument(name, u'')

        if len(value) > KEY_MAX_SIZE:
            raise InvalidValueError(
                'Invalid private key: {}'.format(self.privatekey_filename)
            )
        return value

    @classmethod
    def get_specific_pkey(cls, pkeycls, privatekey, password):
        logging.info('Trying {}'.format(pkeycls.__name__))
        try:
            pkey = pkeycls.from_private_key(io.StringIO(privatekey),
                                            password=password)
        except paramiko.PasswordRequiredException:
            raise
        except paramiko.SSHException:
            pass
        else:
            return pkey

    @classmethod
    def get_pkey_obj(cls, privatekey, password, filename):
        bpass = to_bytes(password) if password else None

        pkey = cls.get_specific_pkey(paramiko.RSAKey, privatekey, bpass)\
            or cls.get_specific_pkey(paramiko.DSSKey, privatekey, bpass)\
            or cls.get_specific_pkey(paramiko.ECDSAKey, privatekey, bpass)\
            or cls.get_specific_pkey(paramiko.Ed25519Key, privatekey, bpass)

        if not pkey:
            if not password:
                error = 'Invalid private key: {}'.format(filename)
            else:
                error = (
                    'Wrong password {!r} for decrypting the private key.'
                ) .format(password)
            raise InvalidValueError(error)

        return pkey

    def get_hostname(self):
        value = self.get_value('hostname')
        if not (is_valid_hostname(value) | is_valid_ip_address(value)):
            raise InvalidValueError('Invalid hostname: {}'.format(value))
        return value

    def get_port(self):
        value = self.get_argument('port', u'')
        if not value:
            return DEFAULT_PORT

        port = to_int(value)
        if port is None or not is_valid_port(port):
            raise InvalidValueError('Invalid port: {}'.format(value))
        return port

    def lookup_hostname(self, hostname, port):
        key = hostname if port == 22 else '[{}]:{}'.format(hostname, port)

        if self.ssh_client._system_host_keys.lookup(key) is None:
            if self.ssh_client._host_keys.lookup(key) is None:
                raise ValueError(
                    'Connection to {}:{} is not allowed.'.format(
                        hostname, port)
                )

    def get_args(self):
        hostname = self.get_hostname()
        port = self.get_port()
        if isinstance(self.policy, paramiko.RejectPolicy):
            self.lookup_hostname(hostname, port)
        username = self.get_value('username')
        password = self.get_argument('password', u'')
        privatekey = self.get_privatekey()
        if privatekey:
            pkey = self.get_pkey_obj(
                privatekey, password, self.privatekey_filename
            )
            password = None
        else:
            pkey = None
        args = (hostname, port, username, password, pkey)
        logging.debug(args)
        return args

    def get_default_encoding(self, ssh):
        try:
            _, stdout, _ = ssh.exec_command('locale charmap')
        except paramiko.SSHException:
            result = None
        else:
            result = to_str(stdout.read().strip())

        return result if result else 'utf-8'

    def ssh_connect(self):
        ssh = self.ssh_client

        try:
            args = self.get_args()
        except InvalidValueError as exc:
            raise tornado.web.HTTPError(400, str(exc))

        dst_addr = (args[0], args[1])
        logging.info('Connecting to {}:{}'.format(*dst_addr))

        try:
            ssh.connect(*args, timeout=6)
        except socket.error:
            raise ValueError('Unable to connect to {}:{}'.format(*dst_addr))
        except paramiko.BadAuthenticationType:
            raise ValueError('Bad authentication type.')
        except paramiko.AuthenticationException:
            raise ValueError('Authentication failed.')
        except paramiko.BadHostKeyException:
            raise ValueError('Bad host key.')

        chan = ssh.invoke_shell(term='xterm')
        chan.setblocking(0)
        worker = Worker(self.loop, ssh, chan, dst_addr)
        worker.src_addr = self.get_client_addr()
        worker.encoding = self.get_default_encoding(ssh)
        return worker

    def ssh_connect_wrapped(self, future):
        try:
            worker = self.ssh_connect()
        except Exception as exc:
            logging.error(traceback.format_exc())
            future.set_exception(exc)
        else:
            future.set_result(worker)

    def head(self):
        pass

    def get(self):
        self.render('index.html', debug=self.debug)

    @tornado.gen.coroutine
    def post(self):
        if self.debug and self.get_argument('error', u''):
            # for testing purpose only
            raise ValueError('Uncaught exception')

        future = Future()
        t = threading.Thread(target=self.ssh_connect_wrapped, args=(future,))
        t.setDaemon(True)
        t.start()

        try:
            worker = yield future
        except (ValueError, paramiko.SSHException) as exc:
            self.result.update(status=str(exc))
        else:
            workers[worker.id] = worker
            self.loop.call_later(DELAY, recycle_worker, worker)
            self.result.update(id=worker.id, encoding=worker.encoding)

        self.write(self.result)


class WsockHandler(MixinHandler, tornado.websocket.WebSocketHandler):

    def initialize(self, loop):
        self.loop = loop
        self.worker_ref = None
        super(WsockHandler, self).initialize()

    def open(self):
        self.src_addr = self.get_client_addr()
        logging.info('Connected from {}:{}'.format(*self.src_addr))
        try:
            worker_id = self.get_value('id')
        except (tornado.web.MissingArgumentError, InvalidValueError) as exc:
            self.close(reason=str(exc))
        else:
            worker = workers.get(worker_id)
            if worker and worker.src_addr[0] == self.src_addr[0]:
                workers.pop(worker.id)
                self.set_nodelay(True)
                worker.set_handler(self)
                self.worker_ref = weakref.ref(worker)
                self.loop.add_handler(worker.fd, worker, IOLoop.READ)
            else:
                self.close(reason='Websocket authentication failed.')

    def on_message(self, message):
        logging.debug('{!r} from {}:{}'.format(message, *self.src_addr))
        worker = self.worker_ref()
        try:
            msg = json.loads(message)
        except JSONDecodeError:
            return

        if not isinstance(msg, dict):
            return

        resize = msg.get('resize')
        if resize and len(resize) == 2:
            try:
                worker.chan.resize_pty(*resize)
            except (TypeError, struct.error, paramiko.SSHException):
                pass

        data = msg.get('data')
        if data and isinstance(data, UnicodeType):
            worker.data_to_dst.append(data)
            worker.on_write()

    def on_close(self):
        if self.close_reason:
            logging.info(
                'Disconnecting to {}:{} with reason: {reason}'.format(
                    *self.src_addr, reason=self.close_reason
                )
            )
        else:
            self.close_reason = 'client disconnected'
            logging.info('Disconnected from {}:{}'.format(*self.src_addr))

        worker = self.worker_ref() if self.worker_ref else None
        if worker:
            worker.close(reason=self.close_reason)
