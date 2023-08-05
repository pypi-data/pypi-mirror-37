import logging
import socket
import sys
import threading
from functools import wraps

import erpc

from .arbitrator import SocketArbitrator
from .system_service import apsbbsys
from .system_service.apsbbsys.common import Coefficients
from .system_service.apsbbsys.common import Colour
from .system_service.apsbbsys.common import LightMode
from .system_service.apsbbsys.common import Timings
from .transport import SocketTransport


def _xport_locked(fn):
    @wraps(fn)
    def _fn(self, *args, **kwargs):
        with self._xport_lock:
            if self._sock is None:
                raise RuntimeError('client not open')
            return fn(self, *args, **kwargs)

    return _fn


class ClientNotificationsHandler(apsbbsys.interface.IClientNotifications):
    def __init__(self, owner, logger):
        self._logger = logger
        self._callbacks = dict(button=None, vehicle=None, barrier=None, icom=None, breach=None, gpio=None)
        self._owner = owner
        self._lock = threading.Lock()
        pass

    @property
    def button_changed_callback(self):
        return self._callbacks['button']

    @button_changed_callback.setter
    def button_changed_callback(self, value):
        with self._lock:
            self._callbacks['button'] = value

    @property
    def vehicle_changed_callback(self):
        return self._callbacks['vehicle']

    @vehicle_changed_callback.setter
    def vehicle_changed_callback(self, value):
        with self._lock:
            self._callbacks['vehicle'] = value

    @property
    def barrier_changed_callback(self):
        return self._callbacks['barrier']

    @barrier_changed_callback.setter
    def barrier_changed_callback(self, value):
        with self._lock:
            self._callbacks['barrier'] = value

    @property
    def intercom_changed_callback(self):
        return self._callbacks['icom']

    @intercom_changed_callback.setter
    def intercom_changed_callback(self, value):
        with self._lock:
            self._callbacks['icom'] = value

    @property
    def breach_changed_callback(self):
        return self._callbacks['breach']

    @breach_changed_callback.setter
    def breach_changed_callback(self, value):
        with self._lock:
            self._callbacks['breach'] = value

    @property
    def gpio_changed_callback(self):
        return self._callbacks['gpio']

    @gpio_changed_callback.setter
    def gpio_changed_callback(self, value):
        with self._lock:
            self._callbacks['gpio'] = value

    def _invoke_callback(self, key, *args, **kwargs):
        with self._lock:
            cb = self._callbacks[key]
            if cb is None:
                self._logger.debug('no callback registered, key=%s', key)
            elif not callable(cb):
                self._logger.warning('registered callback object is not callable, key=%s', key)
            else:
                try:
                    cb(self._owner, *args, **kwargs)
                except:
                    self._logger.exception('caught from callback, key=%s', key)

    def button_changed(self, pressed):
        self._invoke_callback('button', pressed)

    def vehicle_changed(self, status):
        self._invoke_callback('vehicle', status)

    def barrier_changed(self, status):
        self._invoke_callback('barrier', status)

    def intercom_changed(self, active):
        self._invoke_callback('icom', active)

    def breach_changed(self, active):
        self._invoke_callback('breach', active)

    def gpio_changed(self, idx, active):
        self._invoke_callback('gpio', active)


class Client(object):
    """Client of the IPC server.

    TODO
    """

    def __init__(self, *, path=None, logger=None):
        """Initializes client object.

        Parameters
        ----------
        path : address of the server to connect to. May be a UNIX path
            or a TCP address tuple.
        """
        self._sock_path = path
        self._logger = logger or logging.getLogger('.'.join(['apsbblib', 'Client']))

        self._sock = None
        self._xport = None
        self._xport_lock = threading.Lock()
        self._arbitrator = None
        self._manager = None
        self._clients = dict()
        self._server = None
        self._server_thread = None
        self._handler = ClientNotificationsHandler(self, self._logger)
        self._service = apsbbsys.server.ClientNotificationsService(self._handler)

    @property
    def socket_path(self):
        return self._sock_path

    @socket_path.setter
    def socket_path(self, value):
        with self._xport_lock:
            if self._sock is not None:
                raise RuntimeError('socket is open, cannot change path')
            self._sock_path = value

    def open(self):
        """Creates UNIX socket and attempts to connect to the path
        specified at initialization time. Raises RuntimeError if already
        open, forwards exceptions raised during connecting.
        """
        with self._xport_lock:
            if self._sock is not None:
                raise RuntimeError('already open')

            if self._sock_path is None:
                # no specific address to use, try defaults
                if sys.platform.startswith('linux'):
                    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    addr = '\0apsbbserver.socket'
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    addr = ('127.0.0.1', 60498)
            elif type(self._sock_path) is str:
                if sys.platform.startswith('linux'):
                    # string passed, attempt to connect to UNIX socket
                    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    addr = self._sock_path
                else:
                    # Windows platform, interpreting passed string as `ipAddr:port`
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    data = self._sock_path.split(':')
                    if len(data) == 3:
                        addr = (data[0], int(data[1]))
                    elif len(data) == 1:
                        addr = ('127.0.0.1', int(data[0]))
                    else:
                        self._logger.error('invalid server address format: %s', self._sock_path)
                        raise RuntimeError('invalid address')
            elif type(self._sock_path) is tuple:
                # assuming TCP address tuple
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                addr = self._sock_path
            elif type(self._sock_path) is int:
                # assuming port number
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                addr = ('127.0.0.1', self._sock_path)
            else:
                self._logger.error('invalid server address format: %s', self._sock_path)
                raise RuntimeError('invalid address')
            try:
                sock.connect(addr)
            except ConnectionRefusedError as e:
                self._logger.exception('connection to %s refused', addr, exc_info=False)
                raise RuntimeError from e
            self._sock = sock
            del sock

            # socket created and connected successfully
            self._xport = SocketTransport(self._sock)
            self._xport.crc_16 = 0xFFFF
            self._arbitrator = SocketArbitrator(self._xport, erpc.basic_codec.BasicCodec())
            self._manager = erpc.client.ClientManager(self._xport, erpc.basic_codec.BasicCodec)
            self._manager.arbitrator = self._arbitrator

            self._clients['button'] = apsbbsys.client.DeviceButtonClient(self._manager)
            self._clients['buzzer'] = apsbbsys.client.DeviceBuzzerClient(self._manager)
            self._clients['path'] = apsbbsys.client.DevicePathClient(self._manager)
            self._clients['rgb'] = apsbbsys.client.DeviceRGBClient(self._manager)
            self._clients['system'] = apsbbsys.client.DeviceSystemClient(self._manager)
            self._clients['hw_pins'] = apsbbsys.client.HostPinsClient(self._manager)

            self._server = erpc.simple_server.SimpleServer(
                self._arbitrator,
                erpc.basic_codec.BasicCodec
            )
            self._server.add_service(self._service)
            self._server_thread = threading.Thread(
                target=self._client_server,
                name='proxy-erpc-server'
            )
            self._server_thread.start()

    def close(self):
        """Terminates connection."""
        with self._xport_lock:
            if self._sock is None:
                return
            self._server.stop()
            try:
                self._sock.shutdown(socket.SHUT_RDWR)
            except ConnectionResetError:
                pass
            self._sock.close()
            self._server_thread.join()
            # delete object created when opening
            self._server_thread = None
            self._server = None
            self._clients.clear()
            self._manager = None
            self._arbitrator = None
            self._xport = None
            self._sock = None

    def __del__(self):
        self.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def _client_server(self):
        self._logger.info('started')
        try:
            self._server.run()
        except erpc.transport.ConnectionClosed:
            self._logger.info('connection closed')
        except:
            self._logger.exception('exception while running erpc server')
        self._logger.info('returning')
        return

    @property
    def button_changed_callback(self):
        """Callback function invoked when button status changes. The
        callback is invoked with a single argument - a boolean flag
        indicating whether button is pressed or not.
        """
        return self._handler.button_changed_callback

    @button_changed_callback.setter
    def button_changed_callback(self, value):
        self._handler.button_changed_callback = value

    @property
    def vehicle_changed_callback(self):
        """Callback function invoked when vehicle status changes. The
        current PathStatus object is passed to the callback.
        """
        return self._handler.vehicle_changed_callback

    @vehicle_changed_callback.setter
    def vehicle_changed_callback(self, value):
        self._handler.vehicle_changed_callback = value

    @property
    def barrier_changed_callback(self):
        """Callback function invoked when barrier status changes. The
        current PathStatus object is passed to the callback.
        """
        return self._handler.barrier_changed_callback

    @barrier_changed_callback.setter
    def barrier_changed_callback(self, value):
        self._handler.barrier_changed_callback = value

    @property
    def intercom_changed_callback(self):
        """Callback function invoked when intercom button status changes.
        Boolean flag representing current input state is passed as the
        single parameter.
        """
        return self._handler.intercom_changed_callback

    @intercom_changed_callback.setter
    def intercom_changed_callback(self, value):
        self._handler.intercom_changed_callback = value

    @property
    def breach_changed_callback(self):
        """Callback function invoked when breach input status changes.
        Boolean flag representing current input state is passed as the
        single parameter.
        """
        return self._handler.breach_changed_callback

    @breach_changed_callback.setter
    def breach_changed_callback(self, value):
        self._handler.breach_changed_callback = value

    @property
    def gpio_changed_callback(self):
        """Callback function invoked when the status of any of the
        general purpose IO configured as input changes. The callback is
        invoked with two arguments - index of the input changed (integer)
        and its current value (bool).
        """
        return self._handler.gpio_changed_callback

    @gpio_changed_callback.setter
    def gpio_changed_callback(self, value):
        self._handler.gpio_changed_callback = value

    """ SYSTEM PROXIED METHODS """

    @_xport_locked
    def firmware_version(self):
        """Queries the firmware version of the backbone."""
        major = erpc.Reference()
        minor = erpc.Reference()
        maintenance = erpc.Reference()
        crc32 = erpc.Reference()
        ret = self._clients['system'].sys_firmware_version(major, minor, maintenance, crc32)
        if ret == '':
            raise RuntimeError('failed to execute')
        return ret, (major.value, minor.value, maintenance.value), crc32.value

    @_xport_locked
    def software_reset(self):
        """Performs a software reset of the backbone hardware."""
        ret = self._clients['system'].sys_software_reset()
        if ret != 0:
            raise RuntimeError('failed to execute, RC=%d', ret)

    @_xport_locked
    def hardware_reset(self):
        """Performs a hardware reset of the backbone."""
        ret = self._clients['system'].sys_hardware_reset()
        if ret != 0:
            raise RuntimeError('failed to execute, RC=%d', ret)

    """ BUTTON PROXIED METHODS """

    @_xport_locked
    def button_is_pressed(self):
        """Queries button status and returns it as a boolean flag."""
        pressed = erpc.Reference()
        err = self._clients['button'].btn_get_pressed(pressed)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return pressed.value

    @_xport_locked
    def button_press_time(self):
        """Returns integer value indicating how long the button has been
        pressed (in milliseconds). Returns 0 if the button is not pressed.
        """
        press_time = erpc.Reference()
        err = self._clients['button'].btn_get_press_time(press_time)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return press_time.value

    @_xport_locked
    def button_set_enabled(self, enable):
        """Enables or disables button backlight.

        If the backlight is enabled the backbone generates a pulsing waveform
        with the button depressed, the backlight becomes fully lit when
        the button is pressed.

        Parameters
        ----------
        enable : bool
            True to enable, False to disable.
        """
        err = self._clients['button'].btn_set_enabled(enable)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)

    @_xport_locked
    def button_get_enabled(self):
        """Returns boolean flag indicating whether the button backlight is enabled."""
        enabled = erpc.Reference()
        err = self._clients['button'].btn_get_enabled(enabled)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return enabled.value

    """ RGB PROXIED METHODS """

    @_xport_locked
    def rgb_set_colour(self, colour):
        """Configures colour emitted by the RGB module.

        Parameters
        ----------
        colour : Colour
        """
        err = self._clients['rgb'].rgb_set_colour(colour)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)

    @_xport_locked
    def rgb_get_colour(self):
        """Returns colour currently emitted by the RGB module."""
        ref = erpc.Reference()
        err = self._clients['rgb'].rgb_get_colour(ref)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return ref.value

    @_xport_locked
    def rgb_set_timings(self, timings):
        """Configures timings of the waveform generated by the RGB module.

        Parameters
        ----------
        timings : Timings
        """
        err = self._clients['rgb'].rgb_set_timings(timings)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)

    @_xport_locked
    def rgb_get_timings(self):
        """Returns current timings of the waveform generated by the RGB module."""
        ref = erpc.Reference()
        err = self._clients['rgb'].rgb_get_timings(ref)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return ref.value

    @_xport_locked
    def rgb_set_mode(self, mode):
        """Configures mode of the RGB module.

        Parameters
        ----------
        mode : LightMode
        """
        err = self._clients['rgb'].rgb_set_mode(mode)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)

    @_xport_locked
    def rgb_get_mode(self):
        """Returns current mode of the RGB module."""
        ref = erpc.Reference()
        err = self._clients['rgb'].rgb_get_mode(ref)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return ref.value

    @_xport_locked
    def rgb_set_coefficients(self, coeffs):
        """Configures coefficients of the RGB module.

        Parameters
        ----------
        coeffs : Coefficients
        """
        err = self._clients['rgb'].rgb_set_coefficients(coeffs)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)

    @_xport_locked
    def rgb_get_coefficients(self):
        """Returns current coefficients of the waveform generated by the RGB module."""
        ref = erpc.Reference()
        err = self._clients['rgb'].rgb_get_coefficients(ref)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return ref.value

    @_xport_locked
    def rgb_set_config(self, mode, timings, colour, coeffs):
        """Performs a batch configuration of the RGB module.

        Parameters
        ----------
        mode : LightMode
        timings : Timings
        colour : Colour
        coeffs : Coefficients
        """
        err = self._clients['rgb'].rgb_set_config(mode, timings, colour, coeffs)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)

    @_xport_locked
    def rgb_get_config(self):
        """Queries current configuration of the RGB module and returns it as a tuple
        of 4 elements: LightMode, Timings, Colour and Coefficients.
        """
        refs = [erpc.Reference() for v in range(4)]
        err = self._clients['rgb'].rgb_get_config(*refs)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return tuple([ref.value for ref in refs])

    """ PATH PROXIED METHODS """

    @_xport_locked
    def path_clear_result(self):
        """Clears current tracker result."""
        err = self._clients['path'].path_clear_result()
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)

    @_xport_locked
    def path_close(self):
        """Requests closing of the barrier."""
        err = self._clients['path'].path_close()
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)

    @_xport_locked
    def path_get_barrier_timeout(self):
        """Returns current barrier movement timeout value."""
        ref = erpc.Reference()
        err = self._clients['path'].path_get_barrier_timeout(ref)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return ref.value

    @_xport_locked
    def path_get_config(self):
        """Returns current path module configuration as a tuple consisting
        of 3 integers, corresponding to parameters of the path_set_config method.
        """
        refs = [erpc.Reference() for v in range(3)]
        err = self._clients['path'].path_get_config(*refs)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return tuple([ref.value for ref in refs])

    @_xport_locked
    def path_get_loops_hold(self):
        """Returns current loops hold time."""
        ref = erpc.Reference()
        err = self._clients['path'].path_get_loops_hold(ref)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return ref.value

    @_xport_locked
    def path_get_loops_timeout(self):
        """Returns current value of the loops activation timeout."""
        ref = erpc.Reference()
        err = self._clients['path'].path_get_loops_timeout(ref)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return ref.value

    @_xport_locked
    def path_get_result(self):
        """Returns last tracker result (one of TrackerResult values) or
        0 if no result to be reported.
        """
        ref = erpc.Reference()
        err = self._clients['path'].path_get_result(ref)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return ref.value

    @_xport_locked
    def path_get_status(self):
        """Queries current status of the path, returns a PathStatus object."""
        ref = erpc.Reference()
        err = self._clients['path'].path_get_status(ref)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return ref.value

    @_xport_locked
    def path_open(self, force, auto_close):
        """Requests opening of the barrier.

        Parameters
        ----------
        force : bool
            Indicates whether operation is forced, i.e. if the barrier
            movement shall be started even if no vehicle is present at
            loop A.
        auto_close : bool
            Indicates whether the barrier shall be closed after a passthrough
            (or retreat) of the vehicle is detected.
        """
        err = self._clients['path'].path_open(force, auto_close)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)

    """ BUZZER PROXIED METHODS """

    @_xport_locked
    def buzzer_set_frequency(self, frequency):
        """Sets frequency of the sound emitted by the buzzer module.

        NOTE: due to finite resolution of the module the actual frequency may
        slightly differ from the one requested, e.g. when requesting frequency
        of 2kHz the actual frequency (as reported by buzzer_get_frequency method)
        will be 2016Hz.

        Parameters
        ----------
        frequency : int
            Frequency of the emitted sound in Hertz.
        """
        err = self._clients['buzzer'].buzzer_set_frequency(frequency)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)

    @_xport_locked
    def buzzer_get_frequency(self):
        """Returns current frequency of the sound emitted by the buzzer module."""
        ref = erpc.Reference()
        err = self._clients['buzzer'].buzzer_get_frequency(ref)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return ref.value

    @_xport_locked
    def buzzer_enable(self, on_time, off_time, repeat_cnt):
        """Starts operation of the buzzer module.

        Parameters
        ----------
        on_time : int
        off_time : int
        repeat_cnt : int
        """
        err = self._clients['buzzer'].buzzer_enable(on_time, off_time, repeat_cnt)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)

    @_xport_locked
    def buzzer_enable_ack(self):
        """Starts operation of the buzzer module with a predefined parameters."""
        err = self._clients['buzzer'].buzzer_enable_ACK()
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)

    @_xport_locked
    def buzzer_enable_nak(self):
        """Starts operation of the buzzer module with a predefined parameters."""
        err = self._clients['buzzer'].buzzer_enable_NAK()
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)

    """ HOST-PINS PROXIED METHODS """

    @_xport_locked
    def intercom_get(self):
        """Returns logical value of the intercom input."""
        ref = erpc.Reference()
        err = self._clients['hw_pins'].intercom_get(ref)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return ref.value

    @_xport_locked
    def breach_get(self):
        """Returns logical value of the breach input."""
        ref = erpc.Reference()
        err = self._clients['hw_pins'].breach_get(ref)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return ref.value

    @_xport_locked
    def gpio_get(self, idx):
        """Returns logic level of the general purpose port.

        Parameters
        ----------
        idx : int
            Index of the port to query.
        """
        ref = erpc.Reference()
        err = self._clients['hw_pins'].gpio_get(idx, ref)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)
        return ref.value

    @_xport_locked
    def gpio_set(self, idx, enable):
        """Sets status of the general purpose port.

        Parameters
        ----------
        idx : int
            Index of the port to manipulate.
        enable : bool
            Logic state to set.
        """
        err = self._clients['hw_pins'].intercom_get(idx, enable)
        if err != 0:
            raise RuntimeError('failed to execute, RC=%d', err)


