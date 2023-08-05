import json
import logging
import select
import socket
import sys
import threading
from functools import wraps

import jsonrpc

from .device import Device


def _sync_lock(fn):
    @wraps(fn)
    def _fn(self, *args, **kwargs):
        with self._lock:
            return fn(self, *args, **kwargs)

    return _fn


class Server(object):
    class InboundConnection(threading.Thread):
        def __init__(self,
                     index: int,
                     sock: socket.socket,
                     dispatcher: jsonrpc.Dispatcher,
                     logger: logging.Logger = None):
            if not isinstance(sock, socket.socket):
                raise TypeError('sock must be a socket')
            if not isinstance(index, int):
                raise TypeError('index must be an integer')
            if not isinstance(dispatcher, jsonrpc.Dispatcher):
                raise TypeError('dispatcher must be a jsonrpc.Dispatcher')
            self._sock = sock
            self._lock = threading.Lock()
            self._cancel = threading.Event()
            self._dispatcher = dispatcher
            self._logger = logger or logging.getLogger('apsbblib.Servant')
            name = 'servant-{}'.format(index)
            super().__init__(name=name)

        def send_data(self, data):
            offs = 0
            with self._lock:
                while offs < len(data):
                    offs += self._sock.send(data[offs:])

        def stop(self):
            self._cancel.set()
            self.join()

        def run(self):
            self._logger.info('started')
            buf = bytearray()

            while not self._cancel.is_set():
                rlist, *_ = select.select([self._sock], [], [], .5)
                if self._sock not in rlist:
                    continue

                try:
                    tmp = self._sock.recv(64)
                    if tmp == b'':
                        self._logger.info('connection closed')
                        break
                    buf += tmp
                except OSError:
                    self._logger.exception('connection aborted')
                    break

                rsps = []
                while b'\r\n\r\n' in buf:
                    idx = buf.find(b'\r\n\r\n')
                    if idx == 0:
                        buf = buf[4:]
                        continue
                    try:
                        js = buf[:idx].decode()
                    except UnicodeDecodeError:
                        self._logger.exception('failed to decode bytes', exc_info=False)
                        continue
                    finally:
                        buf = buf[idx + 4:]

                    rsp = jsonrpc.JSONRPCResponseManager.handle(js, self._dispatcher)
                    if rsp is not None:
                        rsps.append(rsp)
                try:
                    for rsp in rsps:
                        data = b''.join([rsp.json.encode(), b'\r\n\r\n'])
                        self.send_data(data)
                except OSError:
                    self._logger.exception('failed to send response')
                    break
                finally:
                    del rsps

            self._logger.debug('cleaning up')
            try:
                self._sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            finally:
                self._sock.close()
            self._logger.info('returning')

    def __init__(self, *, port=None, baudrate=None, logger=None):
        self._logger = logger or logging.getLogger('.'.join(['apsbblib', 'Server']))
        self._device = Device(port, baudrate=baudrate)
        self._cancel = threading.Event()
        self._thread = None
        self._thread_lock = threading.Lock()
        self._inbound_conns = []
        self._inbound_counter = 0
        self._inbound_lock = threading.Lock()
        self._socks_lstn = []
        self._dispatcher = jsonrpc.Dispatcher()
        # register methods with the dispatcher
        self._dispatcher.add_method(self.help)
        for fn in [self._device.sys_firmware_version,
                   self._device.sys_get_rtc,
                   self._device.btn_is_pressed,
                   self._device.btn_press_time,
                   self._device.btn_set_enabled,
                   self._device.btn_get_enabled,
                   self._device.rgb_set_colour,
                   self._device.rgb_get_colour,
                   self._device.rgb_set_timings,
                   self._device.rgb_get_timings,
                   self._device.rgb_set_mode,
                   self._device.rgb_get_mode,
                   self._device.rgb_set_coefficients,
                   self._device.rgb_get_coefficients,
                   self._device.rgb_set_config,
                   self._device.rgb_get_config,
                   self._device.path_get_status,
                   self._device.path_open,
                   self._device.path_close,
                   self._device.path_get_barrier_timeout,
                   self._device.path_set_barrier_timeout,
                   self._device.path_get_loopA_timeout,
                   self._device.path_set_loopA_timeout,
                   self._device.path_get_loopB_timeout,
                   self._device.path_set_loopB_timeout,
                   self._device.path_get_loops_hold,
                   self._device.path_set_loops_hold,
                   self._device.path_get_config,
                   self._device.path_set_config,
                   self._device.buzzer_set_frequency,
                   self._device.buzzer_get_frequency,
                   self._device.buzzer_enable,
                   self._device.buzzer_enable_ack,
                   self._device.buzzer_enable_nak,
                   self._device.mdb_execute_command,
                   self._device.mdb_coin_changer_get_status,
                   self._device.mdb_coin_changer_get_setup_data,
                   self._device.mdb_coin_changer_get_expansion_data,
                   self._device.mdb_coin_changer_get_diagnostic_status,
                   self._device.mdb_coin_changer_tube_status,
                   self._device.mdb_coin_changer_coin_type,
                   self._device.mdb_coin_changer_dispense,
                   self._device.mdb_coin_changer_expansion_feature_enable,
                   self._device.mdb_coin_changer_expansion_payout,
                   self._device.mdb_coin_changer_expansion_payout_poll,
                   self._device.mdb_coin_changer_expansion_payout_status,
                   self._device.mdb_coin_changer_expansion_send_controlled_manual_fill_report,
                   self._device.mdb_coin_changer_expansion_send_controlled_manual_payout_report]:
            self._dispatcher.add_method(fn)
        if self._device.has_hardware_pins:
            self._dispatcher.add_method(self.intercom_value)
            self._dispatcher.add_method(self.breach_value)
            self._dispatcher.add_method(self.gpio_value)
            self._dispatcher.add_method(self.gpio_direction)
            self._dispatcher.add_method(self.gpio_invert)
        # register device callbacks
        self._device.barrier_callback = self._barrier_changed_handler
        self._device.vehicle_callback = self._vehicle_changed_handler
        self._device.button_callback = self._button_changed_handler
        if self._device.has_hardware_pins:
            self._device.intercom.register_callback(self._intercom_changed_handler)
            self._device.breach.register_callback(self._breach_changed_handler)
            for pin in self._device.gpios:
                pin.register_callback(self._gpio_changed_handler)

    def _acceptor_thread(self):
        self._logger.info('acceptor thread started')

        while not self._cancel.is_set():
            rlist, *_ = select.select(self._socks_lstn, [], [], .5)
            try:
                for sock in rlist:
                    nsock, remote_ep = sock.accept()
                    if remote_ep is None or len(remote_ep) == 0:
                        self._logger.info('accepted new connection, remote end point unknown')
                    else:
                        self._logger.info('accepted new connection, remote end point is %s', remote_ep)
                    th = Server.InboundConnection(self._inbound_counter,
                                                  nsock,
                                                  self._dispatcher)
                    self._inbound_counter += 1
                    with self._inbound_lock:
                        self._inbound_conns.append(th)
                    th.start()
            except OSError:
                self._logger.exception('failed to accept connection')
                break

            # clean dead threads
            threads_to_remove = []
            for th in self._inbound_conns:
                if not th.is_alive():
                    threads_to_remove.append(th)
            if len(threads_to_remove) > 0:
                with self._inbound_lock:
                    for th in threads_to_remove:
                        th.stop()
                        self._inbound_conns.remove(th)
                self._logger.debug('removed %d dead threads', len(threads_to_remove))
            del threads_to_remove

        self._logger.debug('acceptor thread cleaning up')
        with self._inbound_lock:
            for th in self._inbound_conns:
                th.stop()
            self._inbound_conns.clear()
        for sock in self._socks_lstn:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            finally:
                sock.close()
        self._socks_lstn.clear()
        self._logger.info('acceptor thread returning')

    def _dispatch_notification(self, method: str, params: list):
        self._logger.debug('dispatching notification, method=%s, params=%s', method, params)
        msg = b''.join([json.dumps({'jsonrpc': '2.0',
                                    'method': method,
                                    'params': params}).encode(),
                        b'\r\n\r\n'])
        with self._inbound_lock:
            for th in self._inbound_conns:
                try:
                    th.send_data(msg)
                except OSError:
                    self._logger.exception('failed to dispatch notification')

    def _intercom_changed_handler(self, pin, value):
        self._dispatch_notification('notify-intercom', [value])

    def _breach_changed_handler(self, pin, value):
        self._dispatch_notification('notify-breach', [value])

    def _gpio_changed_handler(self, pin, value):
        idx = None
        for i in range(len(self._device.gpios)):
            if pin == self._device.gpios[i]:
                idx = i
                break
        if idx is None:
            self._logger.error('failed to identify gpio pin, notification dispatching aborted')
            return
        self._dispatch_notification('notify-gpio', [idx, value])

    def _button_changed_handler(self, sender, value):
        self._dispatch_notification('notify-button', [value])

    def _vehicle_changed_handler(self, sender, status):
        self._dispatch_notification('notify-vehicle', status)

    def _barrier_changed_handler(self, sender, status):
        self._dispatch_notification('notify-barrier', status)

    def start(self):
        with self._thread_lock:
            if self._thread is not None:
                raise RuntimeError('server thread already created')

            # assuring single-instance running at any time by exclusive use of socket addresses
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind(('', 60498))
                sock.listen(16)
                self._socks_lstn.append(sock)
            except OSError:
                sock.close()
                self._logger.exception('failed to set-up TCP socket', exc_info=False)
                raise
            finally:
                del sock

            # create UNIX abstract socket if on Linux platform
            if sys.platform.startswith('linux'):
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                try:
                    sock.bind('\0apsbbserver.socket')
                    sock.listen(16)
                    self._socks_lstn.append(sock)
                except OSError:
                    sock.close()
                    self._logger.exception('failed to set-up UNIX socket', exc_info=False)
                    self._socks_lstn[0].close()
                    self._socks_lstn.clear()
                    raise
                finally:
                    del sock

            # sockets created, open device
            try:
                self._device.open()
            except Exception:
                self._logger.exception('failed to open APS BackBone device', exc_info=False)
                for sock in self._socks_lstn:
                    try:
                        sock.shutdown(socket.SHUT_RDWR)
                    except OSError:
                        pass
                    finally:
                        sock.close()
                self._socks_lstn.clear()
                raise

            # all set-up, start thread
            self._thread = threading.Thread(target=self._acceptor_thread, name='acceptor')
            self._thread.start()

    def stop(self):
        with self._thread_lock:
            if self._thread is None:
                return
            self._cancel.set()
            self._thread.join()
            self._thread = None
            self._device.close()
            self._cancel.clear()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False

    def help(self, name: str = None):
        """Return list of available methods or their docstring

        :param str name: name of method whose docstring to return, defaults to None - in that case return list
                         of available methods
        :returns: list of available methods or docstring of queried method
        :rtype: str or list[str]
        :raises KeyError: if method with specified name has not been registered
        """
        if name is None:
            return list(self._dispatcher.keys())
        else:
            return self._dispatcher[name].__doc__

    def intercom_value(self):
        """Return value of the intercom pin"""
        return self._device.intercom.value

    def breach_value(self):
        """Return value of the breach pin"""
        return self._device.breach.value

    def gpio_value(self, idx: int, value=None):
        """Get or set the value of the specified GPIO pin

        :param int idx: index of the pin whose value is to be queried or set
        :param value: v
        """
        if value is None:
            return self._device.gpios[idx].value
        else:
            self._device.gpios[idx].value = value

    def gpio_direction(self, idx, direction=None):
        if direction is None:
            return self._device.gpios[idx].direction
        else:
            self._device.gpios[idx].direction = direction

    def gpio_invert(self, idx, invert=None):
        if invert is None:
            return self._device.gpios[idx].invert
        else:
            self._device.gpios[idx].invert = invert
