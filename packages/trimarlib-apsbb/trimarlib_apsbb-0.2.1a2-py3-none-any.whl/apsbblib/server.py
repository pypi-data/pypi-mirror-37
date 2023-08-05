import logging
import socket
import sys
import threading
from functools import wraps

import erpc

from .apsbackbone import APSBackBone
from .arbitrator import SocketArbitrator
from .system_service import apsbbsys
from .transport import SocketTransport


def _sync_lock(fn):
    @wraps(fn)
    def _fn(self, *args, **kwargs):
        with self._lock:
            return fn(self, *args, **kwargs)

    return _fn


class DeviceSystemHandler(apsbbsys.interface.IDeviceSystem):
    def __init__(self, device: APSBackBone, logger: logging.Logger):
        assert type(device) is APSBackBone
        self._dev = device
        self._logger = logger

    def sys_firmware_version(self, major, minor, maintenance, crc):
        try:
            data = self._dev.sys_firmware_version()
            major.value = data['major']
            minor.value = data['minor']
            maintenance.value = data['maintenance']
            crc.value = data['crc32']
            return data['version']
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return str()

    def sys_software_reset(self):
        try:
            self._dev.sys_reset()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def sys_hardware_reset(self):
        try:
            self._dev.hardware_reset()
            return 0
        except RuntimeError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1


class DeviceButtonHandler(apsbbsys.interface.IDeviceButton):
    def __init__(self, device: APSBackBone, logger: logging.Logger):
        assert type(device) is APSBackBone
        self._dev = device
        self._logger = logger

    def btn_get_pressed(self, pressed):
        try:
            pressed.value = self._dev.btn_is_pressed()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def btn_get_press_time(self, press_time):
        try:
            press_time.value = self._dev.btn_press_time()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def btn_get_enabled(self, enabled):
        try:
            enabled.value = self._dev.btn_get_enabled()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def btn_set_enabled(self, enable):
        try:
            self._dev.btn_set_enabled(enable)
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1


class DeviceRGBHandler(apsbbsys.interface.IDeviceRGB):
    def __init__(self, device: APSBackBone, logger: logging.Logger):
        assert type(device) is APSBackBone
        self._dev = device
        self._logger = logger

    def rgb_get_coefficients(self, coeffs):
        try:
            coeffs.value = self._dev.rgb_get_coefficients()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def rgb_get_colour(self, colour):
        try:
            colour.value = self._dev.rgb_get_colour()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def rgb_get_config(self, mode, timings, colour, coeffs):
        try:
            mode.value, timings.value, colour.value, coeffs.value = self._dev.rgb_get_config()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def rgb_get_mode(self, mode):
        try:
            mode.value = self._dev.rgb_get_mode()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def rgb_get_timings(self, timings):
        try:
            timings.value = self._dev.rgb_get_timings()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def rgb_set_coefficients(self, coeffs):
        try:
            self._dev.rgb_set_coefficients(coeffs)
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def rgb_set_colour(self, colour):
        try:
            self._dev.rgb_set_colour(colour)
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def rgb_set_config(self, mode, timings, colour, coeffs):
        try:
            self._dev.rgb_set_config(mode, timings, colour, coeffs)
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def rgb_set_mode(self, mode):
        try:
            self._dev.rgb_set_mode(mode)
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def rgb_set_timings(self, timings):
        try:
            self._dev.rgb_set_timings(timings)
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1


class DevicePathHandler(apsbbsys.interface.IDevicePath):
    def __init__(self, device: APSBackBone, logger: logging.Logger):
        assert type(device) is APSBackBone
        self._dev = device
        self._logger = logger

    def path_clear_result(self):
        try:
            self._dev.path_clear_result()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def path_close(self):
        try:
            self._dev.path_close()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def path_get_barrier_timeout(self, timeout):
        try:
            timeout.value = self._dev.path_get_barrier_timeout()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def path_get_config(self, barrier_timeout, loops_timeout, loops_hold):
        try:
            barrier_timeout.value, loops_timeout.value, loops_hold.value = self._dev.path_get_config()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def path_get_loops_hold(self, hold_time):
        try:
            hold_time.value = self._dev.path_get_loops_hold()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def path_get_loops_timeout(self, timeout):
        try:
            timeout.value = self._dev.path_get_loops_timeout()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def path_get_result(self, result):
        try:
            result.value = self._dev.path_get_result()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def path_get_status(self, status):
        try:
            status.value = self._dev.path_get_status()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def path_open(self, force, autoClose):
        try:
            self._dev.path_open(force, autoClose)
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1


class DeviceBuzzerHandler(apsbbsys.interface.IDeviceBuzzer):
    def __init__(self, device: APSBackBone, logger: logging.Logger):
        assert type(device) is APSBackBone
        self._dev = device
        self._logger = logger

    def buzzer_enable(self, onTime, offTime, repeat):
        try:
            self._dev.buzzer_enable(onTime, offTime, repeat)
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def buzzer_enable_ACK(self):
        try:
            self._dev.buzzer_enable_ack()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def buzzer_enable_NAK(self):
        try:
            self._dev.buzzer_enable_nak()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def buzzer_get_frequency(self, frequency):
        try:
            frequency.value = self._dev.buzzer_get_frequency()
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1

    def buzzer_set_frequency(self, frequency):
        try:
            self._dev.buzzer_set_frequency(frequency)
            return 0
        except erpc.client.RequestError as e:
            self._logger.exception('execution failed: %s', e, exc_info=False)
            return -1


class HostPinsHandler(apsbbsys.interface.IHostPins):
    def __init__(self, device: APSBackBone, logger: logging.Logger):
        assert type(device) is APSBackBone
        self._dev = device
        self._logger = logger

    def intercom_get(self, pressed):
        try:
            pressed.value = self._dev.intercom.get()
            return 0
        except RuntimeError as e:
            self._logger.exception('operation not supported: %s', e, exc_info=False)
            return -1

    def breach_get(self, active):
        try:
            active.value = self._dev.breach.get()
            return 0
        except RuntimeError as e:
            self._logger.exception('operation not supported: %s', e, exc_info=False)
            return -1

    def gpio_get(self, idx, active):
        try:
            active.value = self._dev.gpios[idx].get()
            return 0
        except IndexError:
            self._logger.exception('index out of range: %d', idx, exc_info=False)
            return -1
        except RuntimeError as e:
            self._logger.exception('operation not supported: %s', e, exc_info=False)
            return -1

    def gpio_set(self, idx, active):
        try:
            self._dev.gpios[idx].set(active)
            return 0
        except IndexError:
            self._logger.exception('index out of range: %d', idx, exc_info=False)
            return -1
        except RuntimeError as e:
            self._logger.exception('operation not supported: %s', e, exc_info=False)
            return -1


class Server(object):
    def __init__(self, *, port=None, baudrate=None, logger=None):
        self._logger = logger or logging.getLogger('.'.join(['apsbblib', 'Server']))
        self._device = APSBackBone(port, baudrate=baudrate)
        self._cancel = threading.Event()
        self._sockets = []
        self._services = (
            apsbbsys.server.DeviceSystemService(DeviceSystemHandler(self._device, self._logger)),
            apsbbsys.server.DeviceButtonService(DeviceButtonHandler(self._device, self._logger)),
            apsbbsys.server.DeviceBuzzerService(DeviceBuzzerHandler(self._device, self._logger)),
            apsbbsys.server.DevicePathService(DevicePathHandler(self._device, self._logger)),
            apsbbsys.server.DeviceRGBService(DeviceRGBHandler(self._device, self._logger)),
            apsbbsys.server.HostPinsService(HostPinsHandler(self._device, self._logger))
        )
        self._clients = []
        self._clients_lock = threading.Lock()
        self._thread = None
        self._thread_lock = threading.Lock()
        self._device.barrier_event = self._barrier_changed_handler
        self._device.vehicle_event = self._vehicle_changed_handler
        self._device.button_event = self._button_changed_handler
        if self._device.has_hardware_pins:
            self._device.intercom.register_callback(self._intercom_changed_handler)
            self._device.breach.register_callback(self._breach_changed_handler)
            for pin in self._device.gpios:
                pin.register_callback(self._gpio_changed_handler)

    def _listener(self):
        self._logger.info('listener thread started')
        for sock in self._sockets:
            sock.listen()
        processor_threads = []
        processor_idx = 0

        while not self._cancel.is_set():
            for sock in self._sockets:
                try:
                    nsock, addr = sock.accept()
                except socket.timeout:
                    nsock = None

                if nsock is not None:
                    if addr is not None and len(addr) > 0:
                        self._logger.debug('accepted new connection from %s', addr)
                    else:
                        self._logger.debug('accepted new connection')
                    nm = 'processor-{}'.format(processor_idx)
                    processor_idx += 1
                    th = threading.Thread(name=nm, target=self._processor, args=(nsock,))
                    processor_threads.append(th)
                    th.start()
                    del nm

            dead_threads = []
            for th in processor_threads:
                if not th.is_alive():
                    dead_threads.append(th)
            if len(dead_threads) > 0:
                self._logger.debug('joining %d dead threads', len(dead_threads))
                for th in dead_threads:
                    th.join()
                    processor_threads.remove(th)
            del dead_threads

        self._logger.debug('cancellation requested')
        for sock in self._sockets:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            sock.close()
        for th in processor_threads:
            th.join()
        self._logger.info('listener thread returning')
        return

    def _processor_server(self, srvr):
        self._logger.info('processor server thread started')
        try:
            srvr.run()
        except erpc.transport.ConnectionClosed:
            self._logger.info('connection closed')
        except:
            self._logger.exception('exception while running erpc server')
        self._logger.info('processor server thread returning')
        return

    def _processor(self, sock):
        self._logger.info('processor thread started')
        xport = SocketTransport(sock)
        xport.crc_16 = 0xFFFF
        arbitrator = SocketArbitrator(xport, erpc.basic_codec.BasicCodec())
        manager = erpc.client.ClientManager(xport, erpc.basic_codec.BasicCodec)
        manager.arbitrator = arbitrator
        c = apsbbsys.client.ClientNotificationsClient(manager)
        with self._clients_lock:
            self._clients.append(c)

        s = erpc.simple_server.SimpleServer(arbitrator, erpc.basic_codec.BasicCodec)
        for service in self._services:
            s.add_service(service)
        sth = threading.Thread(target=self._processor_server,
                               args=(s,),
                               name=('{}-erpc-server'.format(threading.current_thread().name)))
        sth.start()

        while not self._cancel.wait(.5):
            if not sth.is_alive():
                break
        self._logger.debug('cancellation requested')

        s.stop()
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            self._logger.info('connection reset')
        sock.close()
        sth.join()
        with self._clients_lock:
            self._clients.remove(c)

        self._logger.info('processor thread returning')
        return

    def _intercom_changed_handler(self, pin, value):
        self._logger.debug('dispatching notification')
        with self._clients_lock:
            for c in self._clients:
                try:
                    c.intercom_changed(value)
                except:
                    self._logger.exception('failed to dispatch notification to client: %s', c)

    def _breach_changed_handler(self, pin, value):
        self._logger.debug('dispatching breach changed notification')
        with self._clients_lock:
            for c in self._clients:
                try:
                    c.breach_changed(value)
                except:
                    self._logger.exception('failed to dispatch notification to client: %s', c)

    def _gpio_changed_handler(self, pin, value):
        idx = None
        for i in range(len(self._device.gpios)):
            if pin == self._device.gpios[i]:
                idx = i
                break
        if idx is None:
            self._logger.error('failed to identify gpio pin, notification dispatching aborted')
            return
        self._logger.debug('dispatching notification, gpio[%d] ', idx)
        with self._clients_lock:
            for c in self._clients:
                try:
                    c.gpio_changed(idx, value)
                except:
                    self._logger.exception('failed to dispatch notification to client: %s', c)

    def _button_changed_handler(self, sender, value):
        self._logger.debug('dispatching notification from %s', sender)
        with self._clients_lock:
            for c in self._clients:
                try:
                    c.button_changed(value)
                except:
                    self._logger.exception('failed to dispatch notification to client: %s', c)

    def _vehicle_changed_handler(self, sender, status):
        self._logger.debug('dispatching notification from %s', sender)
        with self._clients_lock:
            for c in self._clients:
                try:
                    c.vehicle_changed(status)
                except:
                    self._logger.exception('failed to dispatch notification to client: %s', c)

    def _barrier_changed_handler(self, sender, status):
        self._logger.debug('dispatching notification from %s', sender)
        with self._clients_lock:
            for c in self._clients:
                try:
                    c.barrier_changed(status)
                except:
                    self._logger.exception('failed to dispatch notification to client: %s', c)

    def start(self):
        with self._thread_lock:
            if self._thread is not None:
                raise RuntimeError('server thread already created')
            # assuring single-instance running at any time by exclusive use of socket addresses
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind(('', 60498))
            except OSError as e:
                sock.close()
                self._logger.exception('failed to bind TCP socket: %s', e, exc_info=False)
                raise RuntimeError from e
            sock.settimeout(.5)
            self._sockets.append(sock)
            del sock
            # create UNIX abstract socket if on Linux platform
            if sys.platform.startswith('linux'):
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                try:
                    sock.bind('\0apsbbserver.socket')
                except OSError as e:
                    self._logger.exception('failed to bind UNIX socket: %s', e, exc_info=False)
                    self._sockets[0].close()
                    self._sockets.clear()
                    raise RuntimeError from e
                sock.settimeout(.5)
                self._sockets.append(sock)
                del sock
            # sockets created, open device
            try:
                self._device.open()
            except RuntimeError as e:
                self._logger.exception('failed to open APS BackBone device: %s', e, exc_info=False)
                for sock in self._sockets:
                    sock.shutdown(socket.SHUT_RDWR)
                    sock.close()
                self._sockets.clear()
                raise e
            self._thread = threading.Thread(target=self._listener, name='listener')
            self._thread.start()

    def stop(self):
        with self._thread_lock:
            if self._thread is None:
                return
            self._cancel.set()
            self._thread.join()
            self._thread = None
            self._device.close()
            self._sockets.clear()
            self._cancel.clear()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False
