import logging
import select
import socket
import sys
import threading

from .jrpc import JRPCInvalidMessage
from .jrpc import JRPCMessage, JRPCRequest, JRPCResponse


class Proxy(object):
    """Generic proxy using JSON RPC protocol

    This proxy relies on a presence of ``help`` method at the server side.
    It should return a list of available methods if called without arguments or
    a docstring of a method whose name has been passed. Based on that information
    this proxy exposes remote methods (and their docstrings) as own attributes,
    enabling remote invocation as if the method in question was implemented locally.
    """

    def __init__(self, address=None, *, logger: logging.Logger = None):
        """Initialize Proxy object

        :param address: address of the server to whom a connection is to be made. It may be omitted
                        (default endpoint is used), otherwise the common formats are supported:
                        a UNIX socket path, an integer specifying port number on ``localhost``,
                        a string in format "<address>:<port>", a 2-element tuple ("address", port)
        :type address: str or int or tuple
        :param logging.Logger logger: instance logger
        """
        self._logger = logger or logging.getLogger('apsbblib.Proxy')
        self._lock = threading.Lock()
        self._cancel = threading.Event()
        self._thread = None
        self._sock = None
        self._address = address
        self._remote_methods = []
        self._callbacks = {}
        self._callbacks_lock = threading.Lock()
        self._pending_requests = {}
        self._recv_buffer = bytearray()
        self._timeout = 5.0

    @property
    def address(self):
        """Address of the server"""
        try:
            return self._sock.getpeername()
        except (AttributeError, OSError):
            return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def timeout(self):
        """Time of waiting for response during remote method invocation"""
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = float(value)

    def _make_method(self, name, doc):
        def _remote_method(*args, **kwargs):
            if len(args) > 0 and len(kwargs) > 0:
                raise RuntimeError('protocol does not support positional and keyword arguments at the same time')
            if len(args) > 0:
                params = args
            elif len(kwargs) > 0:
                params = kwargs
            else:
                params = None
            logging.debug('executing dynamically created method: name=%s, args=%s, kwargs=%s', name, args, kwargs)
            return self.invoke_remote(name, params)

        _remote_method.__name__ = name
        _remote_method.__doc__ = doc
        return _remote_method

    def _invoke_callbacks(self, name, *args, **kwargs):
        with self._callbacks_lock:
            if name not in self._callbacks:
                self._logger.warning('no callbacks registered for "%s"', name)
            else:
                for callback in self._callbacks[name]:
                    try:
                        callback(*args, **kwargs)
                    except Exception:
                        self._logger.exception('caught from callback')

    def _do_connect(self):
        if self._address is None:
            # no specific address to use, try defaults
            if sys.platform.startswith('linux'):
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                addr = '\0apsbbserver.socket'
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                addr = ('127.0.0.1', 60498)
        elif type(self._address) is str:
            if sys.platform.startswith('linux'):
                # string passed, attempt to connect to UNIX socket
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                addr = self._address
            else:
                # Windows platform, interpreting passed string as `ipAddr:port`
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                data = self._address.split(':')
                if len(data) == 2:
                    addr = (data[0], int(data[1]))
                elif len(data) == 1:
                    addr = ('127.0.0.1', int(data[0]))
                else:
                    self._logger.error('invalid server address format: %s', self._address)
                    raise RuntimeError('invalid address')
        elif type(self._address) is tuple:
            # assuming TCP address tuple
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            addr = self._address
        elif type(self._address) is int:
            # assuming port number on localhost
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            addr = ('127.0.0.1', self._address)
        else:
            self._logger.error('invalid server address format: %s', self._address)
            raise RuntimeError('invalid address')
        try:
            sock.connect(addr)
        except OSError:
            sock.close()
            raise
        self._sock = sock

    def _do_send(self, request: JRPCRequest):
        data = b''.join([request.json.encode(), b'\r\n\r\n'])
        offs = 0
        while offs < len(data):
            offs += self._sock.send(data[offs:])

    def _do_recv(self, timeout):
        while True:
            while b'\r\n\r\n' in self._recv_buffer:
                idx = self._recv_buffer.find(b'\r\n\r\n')
                if idx == 0:
                    self._recv_buffer = self._recv_buffer[4:]
                    continue
                try:
                    js = self._recv_buffer[:idx].decode()
                    return JRPCMessage.from_json(js)
                except UnicodeDecodeError:
                    self._logger.warning('failed to decode bytes')
                    continue
                finally:
                    self._recv_buffer = self._recv_buffer[idx + 4:]

            rlist, *_ = select.select([self._sock], [], [], timeout)
            if self._sock not in rlist:
                raise TimeoutError()
            del rlist
            tmp = self._sock.recv(64)
            if tmp == b'':
                raise ConnectionAbortedError()
            self._recv_buffer += tmp
            del tmp

    def _do_retrieve_remote_methods(self, timeout):
        request = JRPCRequest('help')
        self._do_send(request)
        while True:
            msg = self._do_recv(timeout)
            if isinstance(msg, JRPCResponse):
                if msg.id == request.id:
                    break
                else:
                    self._logger.warning('expecting response with id=%s, got: "%s"', request.id, msg)
            else:
                self._logger.warning('expecting response, got: "%s"', msg)
        if msg.error is not None:
            self._logger.error('server returned error response: %s', msg.error)
            return
        self._remote_methods = msg.result

        for method in self._remote_methods:
            request = JRPCRequest('help', [method])
            self._do_send(request)
            while True:
                msg = self._do_recv(timeout)
                if isinstance(msg, JRPCResponse):
                    if msg.id == request.id:
                        break
                    else:
                        self._logger.warning('expecting response with id=%s, got: "%s"', request.id, msg)
                else:
                    self._logger.warning('expecting response, got: "%s"', msg)
            if msg.error is not None:
                self._logger.error('server returned error response: %s', msg.error)
                return
            fn = self._make_method(method, msg.result)
            setattr(self, method, fn)

    def _recv_thread(self):
        self._logger.info('proxy recv thread started')

        while not self._cancel.is_set():
            try:
                msg = self._do_recv(timeout=0.5)
            except TimeoutError:
                continue
            except JRPCInvalidMessage:
                self._logger.exception('failed to parse JSON RPC message')
                continue
            except OSError:
                self._logger.exception('connection terminated')
                break

            if isinstance(msg, JRPCRequest):
                if isinstance(msg.params, list):
                    self._invoke_callbacks(msg.method, *msg.params)
                elif isinstance(msg.params, dict):
                    self._invoke_callbacks(msg.method, **msg.params)
                else:
                    self._invoke_callbacks(msg.method)
            elif isinstance(msg, JRPCResponse):
                try:
                    self._pending_requests[msg.id]['response'] = msg
                    self._pending_requests[msg.id]['event'].set()
                except KeyError:
                    self._logger.warning('matching pending request not found, response = "%s"', msg.json)
            else:
                self._logger.error('unexpected condition')

        self._logger.debug('proxy recv thread clean up')
        # finalize all pending requests
        for key, item in self._pending_requests:
            item['event'].set()
        self._logger.debug('proxy thread returning')

    def open(self):
        """Open connection to the server

        Attempts to connect to the server (whose address has been specified at initialization time or
        via :ref:`Server.address` property), tries to retrieve available remote methods and add them as
        attributes of the current object. Finally, it starts receiving thread.

        :raises OSError: if connection attempt failed
        """

        with self._lock:
            if self._sock is not None:
                raise RuntimeError('socket already open')

            self._do_connect()
            try:
                self._do_retrieve_remote_methods(5)
            except TimeoutError:
                self._logger.exception('timeout while retrieving remote methods', exc_info=False)
            except OSError:
                try:
                    self._sock.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                finally:
                    self._sock.close()
                self._sock = None
                raise
            # start rx thread
            self._thread = threading.Thread(name='proxy-recv', target=self._recv_thread)
            self._thread.start()

    def close(self):
        """Close connection to the server

        Terminates receiving thread, shuts down and closes socket, deletes exposed
        remote methods (that have been added when connection was opened).
        """

        with self._lock:
            if self._sock is None:
                return

            self._cancel.set()
            self._thread.join()
            self._thread = None
            try:
                self._sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            finally:
                self._sock.close()
                self._sock = None
            for method in self._remote_methods:
                try:
                    delattr(self, method)
                except AttributeError:
                    pass
            self._remote_methods.clear()
            self._cancel.clear()

    def invoke_remote(self, method: str, params=None):
        """Invoke remote method and return result

        Creates JSON RPC request, sends it to the server and awaits response for a time
        specified via :ref:`Server.timeout` property.

        :param str method: name of method to invoke
        :param params: parameters to include in the JSON RPC message
        :type params: a list, a tuple or a dictionary, defaults to None
        :returns: `result` field of the received response message
        :raises TimeoutError: no response has been received but connection is still open
        :raises ConnectionAbortedError: connection has been closed
        :raises RuntimeError: server responded with an error, received error object is passed as argument
        """

        request = JRPCRequest(method, params)
        self._pending_requests[request.id] = dict(response=None, event=threading.Event())
        try:
            with self._lock:
                self._do_send(request)
            # request transmitted, wait for response
            if not self._pending_requests[request.id]['event'].wait(self.timeout):
                raise TimeoutError()
            response = self._pending_requests[request.id]['response']
        finally:
            del self._pending_requests[request.id]

        if response is None:
            raise ConnectionAbortedError()
        elif response.error is not None:
            raise RuntimeError(response.error)
        return response.result

    def register_callback(self, fn, name):
        """Register callback object for server notification

        :param fn: callback object to be registered
        :type fn: callable
        :param name: namespaces for which *fn* is to be registered
        :type name: str or list[str] or tuple(str)
        :raises TypeError: if fn is not callable or name is not a string or an iterable of such
        """

        if not callable(fn):
            raise TypeError('callback object must be callable')
        if not isinstance(name, (list, tuple)):
            name = [name]
        for nm in name:
            if not isinstance(nm, str):
                raise TypeError('name must be a string')
            with self._callbacks_lock:
                if nm not in self._callbacks:
                    self._callbacks[nm] = []
                if fn in self._callbacks[nm]:
                    self._logger.warning('callback function %s is already registered for name "%s"', fn, nm)
                else:
                    self._callbacks[nm].append(fn)

    def unregister_callback(self, fn, name=None):
        """Unregister callback object

        If *name* is None, an attempt is made to remove *fn* from all methods; otherwise it is removed
        only from the specified namespaces.

        :param fn: callback object
        :type fn: callable
        :param name: namespaces for which *fn* is to be unregistered
        :type name: str or list[str] or tuple(str)
        """

        with self._callbacks_lock:
            if name is not None:
                if not isinstance(name, (list, tuple)):
                    name = [name]
                for nm in name:
                    try:
                        self._callbacks[nm].remove(fn)
                        if len(self._callbacks[nm]) == 0:
                            del self._callbacks[nm]
                    except KeyError:
                        self._logger.warning('no callbacks registered for "%s"', nm)
                    except ValueError:
                        self._logger.warning('%s not registered for "%s"', fn, nm)
            else:
                keys = list(self._callbacks.keys())
                for name in keys:
                    try:
                        self._callbacks[name].remove(fn)
                        if len(self._callbacks[name]) == 0:
                            del self._callbacks[name]
                    except ValueError:
                        pass

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
