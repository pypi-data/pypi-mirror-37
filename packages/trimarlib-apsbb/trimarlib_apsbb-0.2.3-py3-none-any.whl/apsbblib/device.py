import logging
import struct
import threading
import time
from functools import wraps

import erpc
import serial
import webcolors

from .device_service.apsbb import common, client
from .transport import SerialTransport

try:
    import sysfsgpio
except ImportError:
    sysfsgpio = None


def _sync_xport(fn):
    @wraps(fn)
    def _fn(self, *args, **kwargs):
        with self._xport_lock:
            if self._xport is None:
                raise RuntimeError('device is not open!')
            return fn(self, *args, **kwargs)

    return _fn


def _tracker_result_to_str(result):
    if result == common.TrackerResult.ePassthroughOK:
        ret = 'passthrough-ok'
    elif result == common.TrackerResult.ePassthroughRetreated:
        ret = 'passthrough-retreated'
    elif result == common.TrackerResult.ePassthroughWrongWay:
        ret = 'passthrough-wrongway'
    else:
        ret = None
    return ret


def _path_status_to_dict(status):
    ret = dict()

    if status.vehicle_position == common.VehiclePosition.eVehicleNone:
        ret['vehicle_position'] = 'none'
    elif status.vehicle_position == common.VehiclePosition.eVehicleA:
        ret['vehicle_position'] = 'A'
    elif status.vehicle_position == common.VehiclePosition.eVehicleB:
        ret['vehicle_position'] = 'B'
    elif status.vehicle_position == common.VehiclePosition.eVehicleAB:
        ret['vehicle_position'] = 'AB'
    else:
        ret['vehicle_position'] = 'unknown'

    ret['loopA_timeout'] = status.loopA_timeout
    ret['loopB_timeout'] = status.loopB_timeout
    ret['barrier_timeout'] = status.barrier_timeout

    if status.barrier_position == common.BarrierPosition.eBarPosOpen:
        ret['barrier_position'] = 'open'
    elif status.barrier_position == common.BarrierPosition.eBarPosClosed:
        ret['barrier_position'] = 'closed'
    elif status.barrier_position == common.BarrierPosition.eBarPosError:
        ret['barrier_position'] = 'error'
    else:
        ret['barrier_position'] = 'unknown'

    if status.barrier_action == common.BarrierAction.eBarActIdle:
        ret['barrier_action'] = 'idle'
    elif status.barrier_action == common.BarrierAction.eBarActOpening:
        ret['barrier_action'] = 'opening'
    elif status.barrier_action == common.BarrierAction.eBarActClosing:
        ret['barrier_action'] = 'closing'
    elif status.barrier_action == common.BarrierAction.eBarActWaiting:
        ret['barrier_action'] = 'waiting'
    elif status.barrier_action == common.BarrierAction.eBarActAutoStopped:
        ret['barrier_action'] = 'auto-stopped'
    else:
        ret['barrier_action'] = 'unknown'

    ret['tracker_result'] = _tracker_result_to_str(status.tracker_result)

    return ret


class Device(object):
    def __init__(self, port='/dev/ttyS1', *, baudrate=115200, logger=None):
        if logger is None:
            self._logger = logging.getLogger('apsbblib.Device')
        elif isinstance(logger, logging.Logger):
            self._logger = logger
        else:
            raise TypeError('logger must be an instance of logging.Logger')
        self._device_closing = threading.Event()
        self._xport_lock = threading.Lock()

        self._xport = SerialTransport(port, baudrate,
                                      timeout=2.5, exclusive=True, stopbits=serial.STOPBITS_TWO, do_not_open=True)
        self._xport.crc_16 = 0xFFFF
        self._manager = erpc.client.ClientManager(self._xport, erpc.basic_codec.BasicCodec)
        self._sys_client = client.SystemClient(self._manager)
        self._rgb_client = client.RGBClient(self._manager)
        self._path_client = client.PathClient(self._manager)
        self._btn_client = client.ButtonClient(self._manager)
        self._buzz_client = client.BuzzerClient(self._manager)
        self._mdb_client = client.MDBClient(self._manager)

        if sysfsgpio is None:
            self._logger.warning('module sysfsgpio not loaded, using dummy pins')
            self._pins = None
        else:
            self._pins = dict(boot=sysfsgpio.Pin('PA7', 'out'),
                              breach=sysfsgpio.Pin('PD14'),
                              gpios=(sysfsgpio.Pin('PA10'),
                                     sysfsgpio.Pin('PA20'),
                                     sysfsgpio.Pin('PA21'),
                                     sysfsgpio.Pin('PC4')),
                              icom=sysfsgpio.Pin('PC7'),
                              irq=sysfsgpio.Pin('PA9'),
                              rst=sysfsgpio.Pin('PA8', 'out'))
            self._pins['irq'].register_callback(self._irq_pin_callback)

        self._event_callbacks = dict(vehicle=None, barrier=None, button=None)
        self._event_callbacks['coin-changer.status'] = None
        self._event_callbacks['coin-changer.diagnostic'] = None
        self._event_callbacks['coin-changer.tube'] = None
        self._event_callbacks_lock = threading.Lock()

        self._dispatcher_event = threading.Event()
        self._dispatcher_thread = None

    def _invoke_callback(self, key, *args, **kwargs):
        cb = self._event_callbacks[key]
        if cb is None:
            self._logger.info('no callback registered for %s event', key)
        elif not callable(cb):
            self._logger.error('callback object for %s event is not callable! %s', key, cb)
        else:
            try:
                cb(self, *args, **kwargs)
            except:
                self._logger.exception('caught from %s event callback', key)
        return

    def _irq_pin_callback(self, pin, v):
        if pin == self._pins['irq']:
            if v == 1:
                self._logger.debug('new interrupt from the backbone')
                self._dispatcher_event.set()
            else:
                self._logger.debug('backbone interrupt line cleared')
        else:
            self._logger.warning('callback from unexpected source: %s, %d', pin.pinname(), v)

    def _dispatcher_fun(self):
        self._logger.debug('thread started')
        path_status = None
        button_pressed = None
        cc_diag_status = None
        cc_status = None
        cc_tube_full = None
        cc_tube_status = None
        cc_tube_sum = None

        while not self._device_closing.is_set():
            if self._pins is None:
                if self._device_closing.wait(1.0):
                    continue
            elif not self._dispatcher_event.wait(0.5) and self._pins['irq'].value == 0:
                continue
            self._dispatcher_event.clear()

            if not self._xport_lock.acquire(timeout=1):
                continue
            try:
                irq = self._sys_client.sys_get_interrupt()
            except (struct.error, erpc.client.RequestError, ValueError, TimeoutError) as e:
                self._logger.exception('failed to read interrupt register: %s, repr = %s', e, repr(e), exc_info=False)
                time.sleep(.5)
                self._xport._serial.flushInput()
                self._xport_lock.release()
                continue
            except serial.SerialException:
                self._logger.exception('serial port error', exc_info=False)
                self._xport_lock.release()
                break

            if irq == 0:
                self._xport_lock.release()
            else:
                self._logger.debug('got event, irq=%d', irq)
                try:
                    if (irq & (common.InterruptBits.eIntBarrier
                               | common.InterruptBits.eIntVehicle)) != 0:
                        status = erpc.Reference()
                        self._path_client.path_get_status(status)
                        self._path_client.path_clear_result()
                        path_status = _path_status_to_dict(status.value)
                        del status
                        self._logger.debug('new path status is %s', path_status)
                    if (irq & common.InterruptBits.eIntButton) != 0:
                        button_pressed = self._btn_client.btn_is_pressed()
                        self._logger.debug('new button status is %s', button_pressed)
                    if (irq & common.InterruptBits.eIntCoinChangerStatus) != 0:
                        cc_status = self._mdb_client.mdb_coin_changer_get_status()
                        self._logger.debug('new Coin Changer status is %02X', cc_status)
                    if (irq & common.InterruptBits.eIntCoinChangerDiagnosticStatus) != 0:
                        cc_diag_status = erpc.Reference()
                        self._mdb_client.mdb_coin_changer_get_diagnostic_status(cc_diag_status)
                        cc_diag_status = cc_diag_status.value
                        self._logger.debug('new Coin Changer diagnostic status is %02X-%02X', *cc_diag_status)
                    if (irq & common.InterruptBits.eIntCoinChangerTubeStatus) != 0:
                        cc_tube_full = erpc.Reference()
                        cc_tube_status = erpc.Reference()
                        setup_data = erpc.Reference()
                        self._mdb_client.mdb_coin_changer_tube_status(cc_tube_full, cc_tube_status)
                        self._mdb_client.mdb_coin_changer_get_setup_data(setup_data)
                        cc_tube_full = cc_tube_full.value
                        cc_tube_status = cc_tube_status.value
                        setup_data = setup_data.value
                        cc_tube_sum = 0.0
                        for i in range(len(cc_tube_status)):
                            cc_tube_sum += cc_tube_status[i] * setup_data.coin_credit[
                                i] * setup_data.scaling_factor / 10 ** setup_data.decimal_places
                        self._logger.debug('new Coin Changer tube status is: TOTAL=%s%.2f, FULL=%02X, COUNT=%s',
                                           '>' if cc_tube_full != 0 else '', cc_tube_sum, cc_tube_full, cc_tube_status)
                        del setup_data

                except (struct.error, erpc.client.RequestError) as e:
                    self._logger.exception('failed to read device status: %s', e, exc_info=False)
                    self._xport._serial.reset_input_buffer()
                    self._xport_lock.release()
                    continue
                except serial.SerialException:
                    self._logger.exception('serial port error', exc_info=False)
                    self._xport_lock.release()
                    break

                try:
                    self._sys_client.sys_clear_interrupt(irq)
                except (struct.error, erpc.client.RequestError) as e:
                    self._logger.exception('failed to clear interrupt register: %s', e, exc_info=False)
                    self._xport._serial.reset_input_buffer()
                    continue
                except serial.SerialException:
                    self._logger.exception('serial port error', exc_info=False)
                    break
                finally:
                    self._xport_lock.release()

                with self._event_callbacks_lock:
                    if (irq & common.InterruptBits.eIntBarrier) != 0:
                        self._logger.debug('dispatching barrier event')
                        self._invoke_callback('barrier', path_status)
                    if (irq & common.InterruptBits.eIntVehicle) != 0:
                        self._logger.debug('dispatching vehicle event')
                        self._invoke_callback('vehicle', path_status)
                    if (irq & common.InterruptBits.eIntButton) != 0:
                        self._logger.debug('dispatching button event')
                        self._invoke_callback('button', button_pressed)
                    if (irq & common.InterruptBits.eIntCoinChangerStatus) != 0:
                        self._logger.debug('dispatching CoinChanger status event')
                        self._invoke_callback('coin-changer.status', cc_status)
                    if (irq & common.InterruptBits.eIntCoinChangerDiagnosticStatus) != 0:
                        self._logger.debug('dispatching CoinChanger diagnostic status event')
                        self._invoke_callback('coin-changer.diagnostic', cc_diag_status)
                    if (irq & common.InterruptBits.eIntCoinChangerTubeStatus) != 0:
                        self._logger.debug('dispatching CoinChanger tube status event')
                        self._invoke_callback('coin-changer.tube', cc_tube_sum, cc_tube_full, cc_tube_status)

        self._logger.debug('thread returning')
        return

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def open(self):
        with self._xport_lock:
            if self._dispatcher_thread is not None:
                raise RuntimeError('device already open')
            self._xport._serial.open()
            self._dispatcher_event.set()
            self._dispatcher_thread = threading.Thread(
                name='dispatcher',
                target=self._dispatcher_fun
            )
            if self._pins is not None:
                self._pins['irq'].enabled = True
                self._pins['icom'].enabled = True
                self._pins['breach'].enabled = True
            self._dispatcher_thread.start()
        return

    def close(self):
        with self._xport_lock:
            if self._dispatcher_thread is None:
                return
            if self._pins is not None:
                self._pins['irq'].enabled = False
                self._pins['icom'].enabled = False
                self._pins['breach'].enabled = False
            self._device_closing.set()
            self._dispatcher_thread.join()
            self._dispatcher_thread = None
            self._device_closing.clear()
            try:
                self._xport.close()
            except:
                pass
        return

    @property
    def has_hardware_pins(self):
        if sysfsgpio is None:
            return False
        return True

    @property
    def intercom(self):
        """Getter of the underlying Pin object"""
        if self._pins is None:
            raise RuntimeError('hardware pins not available')
        return self._pins['icom']

    @property
    def breach(self):
        """Getter of the underlying Pin object"""
        if self._pins is None:
            raise RuntimeError('hardware pins not available')
        return self._pins['breach']

    @property
    def barrier_callback(self):
        return self._event_callbacks['barrier']

    @barrier_callback.setter
    def barrier_callback(self, value):
        with self._event_callbacks_lock:
            self._event_callbacks['barrier'] = value

    @property
    def vehicle_callback(self):
        return self._event_callbacks['vehicle']

    @vehicle_callback.setter
    def vehicle_callback(self, value):
        with self._event_callbacks_lock:
            self._event_callbacks['vehicle'] = value

    @property
    def button_callback(self):
        return self._event_callbacks['button']

    @button_callback.setter
    def button_callback(self, value):
        with self._event_callbacks_lock:
            self._event_callbacks['button'] = value

    @property
    def coin_changer_status_callback(self):
        return self._event_callbacks['coin-changer.status']

    @coin_changer_status_callback.setter
    def coin_changer_status_callback(self, value):
        with self._event_callbacks_lock:
            self._event_callbacks['coin-changer.status'] = value

    @property
    def coin_changer_diagnostic_callback(self):
        return self._event_callbacks['coin-changer.diagnostic']

    @coin_changer_diagnostic_callback.setter
    def coin_changer_diagnostic_callback(self, value):
        with self._event_callbacks_lock:
            self._event_callbacks['coin-changer.diagnostic'] = value

    @property
    def coin_changer_tube_callback(self):
        return self._event_callbacks['coin-changer.tube']

    @coin_changer_tube_callback.setter
    def coin_changer_tube_callback(self, value):
        with self._event_callbacks_lock:
            self._event_callbacks['coin-changer.tube'] = value

    @property
    def gpios(self):
        if self._pins is None:
            raise RuntimeError('hardware pins not available')
        return self._pins['gpios']

    @_sync_xport
    def hardware_reset(self):
        """Hardware reset of the backbone

        Asserts board reset signal, holds it for .5s, deasserts and
        waits 1s for boot to complete."""
        if self._pins is None:
            raise RuntimeError('operation not supported, hardware pins not available')
        self._pins['rst'].value = 1
        time.sleep(.5)
        self._pins['rst'].value = 0
        time.sleep(1)

    # ===========
    # SYS METHODS
    # ===========

    @_sync_xport
    def sys_firmware_version(self):
        major = erpc.Reference()
        minor = erpc.Reference()
        maintenance = erpc.Reference()
        crc = erpc.Reference()
        ver = self._sys_client.sys_firmware_version(major, minor, maintenance, crc)
        ret = dict(version=ver,
                   major=major.value,
                   minor=minor.value,
                   maintenance=maintenance.value,
                   crc32=crc.value)
        return ret

    @_sync_xport
    def sys_reset(self):
        self._sys_client.sys_reset()
        time.sleep(1)
        return

    @_sync_xport
    def sys_bootloader(self):
        self._sys_client.sys_bootloader()
        return

    @_sync_xport
    def sys_set_rtc(self, seconds=None):
        if seconds is None:
            seconds = time.time()
        self._sys_client.sys_set_rtc(common.Timeval(int(seconds), 0))
        return

    @_sync_xport
    def sys_get_rtc(self):
        tv = erpc.Reference()
        self._sys_client.sys_get_rtc(tv)
        ret = tv.value.secs + tv.value.usecs / 1e6
        return ret

    @_sync_xport
    def sys_get_interrupt(self):
        return self._sys_client.sys_get_interrupt()

    @_sync_xport
    def sys_clear_interrupt(self, mask=common.InterruptBits.eIntAll):
        self._sys_client.sys_clear_interrupt(mask)
        return

    # ===========
    # BTN METHODS
    # ===========

    @_sync_xport
    def btn_is_pressed(self):
        return self._btn_client.btn_is_pressed()

    @_sync_xport
    def btn_press_time(self):
        return self._btn_client.btn_press_time()

    @_sync_xport
    def btn_set_invert(self, enable):
        self._btn_client.btn_set_invert(enable)

    @_sync_xport
    def btn_get_invert(self):
        return self._btn_client.btn_get_invert()

    @_sync_xport
    def btn_set_enabled(self, enable):
        self._btn_client.btn_set_enabled(enable)

    @_sync_xport
    def btn_get_enabled(self):
        return self._btn_client.btn_get_enabled()

    @_sync_xport
    def btn_set_config(self, enable: bool, invert: bool):
        self._btn_client.btn_set_config(enable, invert)

    @_sync_xport
    def btn_get_config(self):
        enable = erpc.Reference()
        invert = erpc.Reference()
        self._btn_client.btn_get_config(enable, invert)
        return enable.value, invert.value

    # ===========
    # RGB METHODS
    # ===========

    @_sync_xport
    def rgb_set_colour(self, colour):
        """Set colour emitted by the RGB diode

        :param colour:
        :type colour: str or dict or int or common.Colour
        """
        if isinstance(colour, str):
            rgb = webcolors.name_to_rgb(colour)
            colour = common.Colour(rgb.red, rgb.green, rgb.blue)
        elif isinstance(colour, int):
            val = colour
            colour = common.Colour(val & 0xFF, (val >> 8) & 0xFF, (val >> 16) & 0xFF)
        elif isinstance(colour, dict):
            val = colour
            colour = common.Colour(val['red'], val['green'], val['blue'])
        self._rgb_client.rgb_set_colour(colour)

    @_sync_xport
    def rgb_get_colour(self) -> dict:
        """Get colour emitted by the RGB diode and return it as a dictionary"""
        colour = erpc.Reference()
        self._rgb_client.rgb_get_colour(colour)
        return dict(red=colour.value.r, green=colour.value.g, blue=colour.value.b)

    @_sync_xport
    def rgb_set_timings(self, timings):
        if isinstance(timings, (tuple, list)):
            val = timings
            timings = common.Timings(*val)
        elif isinstance(timings, dict):
            val = timings
            timings = common.Timings(val['onTime'], val['offTime'], val['stepTime'])
        self._rgb_client.rgb_set_timings(timings)

    @_sync_xport
    def rgb_get_timings(self) -> dict:
        timings = erpc.Reference()
        self._rgb_client.rgb_get_timings(timings)
        return dict(onTime=timings.value.onTime, offTime=timings.value.offTime, stepTime=timings.value.stepTime)

    @_sync_xport
    def rgb_set_mode(self, mode):
        if isinstance(mode, str):
            if mode.lower() == 'off':
                mode = common.LightMode.eLightOff
            elif mode.lower() == 'on':
                mode = common.LightMode.eLightOn
            elif mode.lower() == 'pulsing':
                mode = common.LightMode.eLightPulsing
            else:
                raise ValueError('unknown RGB mode: "{}", possible values are "off", "on" and "pulsing"'.format(mode))
        self._rgb_client.rgb_set_mode(mode)

    @_sync_xport
    def rgb_get_mode(self) -> str:
        mode = self._rgb_client.rgb_get_mode()
        if mode == common.LightMode.eLightOff:
            ret = 'off'
        elif mode == common.LightMode.eLightOn:
            ret = 'on'
        elif mode == common.LightMode.eLightPulsing:
            ret = 'pulsing'
        else:
            ret = 'unknown'
        return ret

    @_sync_xport
    def rgb_set_coefficients(self, coeffs):
        if isinstance(coeffs, (tuple, list)):
            coeffs = common.Coefficients(*coeffs)
        elif isinstance(coeffs, dict):
            val = coeffs
            coeffs = common.Coefficients(val['A'], val['B'])
        self._rgb_client.rgb_set_coefficients(coeffs)

    @_sync_xport
    def rgb_get_coefficients(self) -> dict:
        coeffs = erpc.Reference()
        self._rgb_client.rgb_get_coefficients(coeffs)
        return dict(A=coeffs.value.A, B=coeffs.value.B)

    @_sync_xport
    def rgb_set_config(self, mode, timings, colour, coeffs):
        if isinstance(mode, str):
            if mode.lower() == 'off':
                mode = common.LightMode.eLightOff
            elif mode.lower() == 'on':
                mode = common.LightMode.eLightOn
            elif mode.lower() == 'pulsing':
                mode = common.LightMode.eLightPulsing
            else:
                raise ValueError('unknown RGB mode: "{}", possible values are "off", "on" and "pulsing"'.format(mode))

        if isinstance(timings, (tuple, list)):
            val = timings
            timings = common.Timings(*val)
        elif isinstance(timings, dict):
            val = timings
            timings = common.Timings(val['onTime'], val['offTime'], val['stepTime'])

        if isinstance(colour, str):
            rgb = webcolors.name_to_rgb(colour)
            colour = common.Colour(rgb.red, rgb.green, rgb.blue)
        elif isinstance(colour, int):
            val = colour
            colour = common.Colour(val & 0xFF, (val >> 8) & 0xFF, (val >> 16) & 0xFF)
        elif isinstance(colour, dict):
            val = colour
            colour = common.Colour(val['red'], val['green'], val['blue'])

        if isinstance(coeffs, (tuple, list)):
            coeffs = common.Coefficients(*coeffs)
        elif isinstance(coeffs, dict):
            val = coeffs
            coeffs = common.Coefficients(val['A'], val['B'])

        self._rgb_client.rgb_set_config(mode, timings, colour, coeffs)

    @_sync_xport
    def rgb_get_config(self) -> dict:
        mode = erpc.Reference()
        timings = erpc.Reference()
        colour = erpc.Reference()
        coeffs = erpc.Reference()
        self._rgb_client.rgb_get_config(mode, timings, colour, coeffs)
        ret = dict()
        if mode.value == common.LightMode.eLightOff:
            ret['mode'] = 'off'
        elif mode.value == common.LightMode.eLightOn:
            ret['mode'] = 'on'
        elif mode.value == common.LightMode.eLightPulsing:
            ret['mode'] = 'pulsing'
        else:
            ret['mode'] = 'unknown'
        ret['timings'] = dict(onTime=timings.value.onTime,
                              offTime=timings.value.offTime,
                              stepTime=timings.value.stepTime)
        ret['colour'] = dict(red=colour.value.r,
                             green=colour.value.g,
                             blue=colour.value.b)
        ret['coefficients'] = dict(A=coeffs.value.A, B=coeffs.value.B)
        return ret

    # ============
    # PATH METHODS
    # ============

    @_sync_xport
    def path_get_status(self) -> dict:
        status = erpc.Reference()
        self._path_client.path_get_status(status)
        return _path_status_to_dict(status.value)

    @_sync_xport
    def path_open(self, force: bool = False, auto_close: bool = True):
        self._path_client.path_open(force, auto_close)

    @_sync_xport
    def path_close(self):
        self._path_client.path_close()

    @_sync_xport
    def path_set_barrier_timeout(self, timeout: int):
        self._path_client.path_set_barrier_timeout(timeout)

    @_sync_xport
    def path_get_barrier_timeout(self) -> int:
        return self._path_client.path_get_barrier_timeout()

    @_sync_xport
    def path_set_loopA_timeout(self, timeout: int):
        self._path_client.path_set_loopA_timeout(timeout)

    @_sync_xport
    def path_get_loopA_timeout(self) -> int:
        return self._path_client.path_get_loopA_timeout()

    @_sync_xport
    def path_set_loopB_timeout(self, timeout: int):
        self._path_client.path_set_loopB_timeout(timeout)

    @_sync_xport
    def path_get_loopB_timeout(self) -> int:
        return self._path_client.path_get_loopB_timeout()

    @_sync_xport
    def path_set_loops_hold(self, time_ms: int):
        self._path_client.path_set_loops_hold(time_ms)

    @_sync_xport
    def path_get_loops_hold(self) -> int:
        return self._path_client.path_get_loops_hold()

    @_sync_xport
    def path_get_result(self) -> str:
        result = self._path_client.path_get_result()
        return _tracker_result_to_str(result)

    @_sync_xport
    def path_clear_result(self):
        self._path_client.path_clear_result()

    @_sync_xport
    def path_set_config(self, barrier_timeout: int,
                        loopA_timeout: int,
                        loopB_timeout: int,
                        loops_hold: int):
        self._path_client.path_set_config(barrier_timeout,
                                          loopA_timeout,
                                          loopB_timeout,
                                          loops_hold)

    @_sync_xport
    def path_get_config(self) -> dict:
        barrier_timeout = erpc.Reference()
        loopA_timeout = erpc.Reference()
        loopB_timeout = erpc.Reference()
        loops_hold = erpc.Reference()
        self._path_client.path_get_config(barrier_timeout,
                                          loopA_timeout,
                                          loopB_timeout,
                                          loops_hold)
        return dict(barrier_timeout=barrier_timeout.value,
                    loopA_timeout=loopA_timeout.value,
                    loopB_timeout=loopB_timeout.value,
                    loops_hold=loops_hold.value)

    # ==============
    # BUZZER METHODS
    # ==============

    @_sync_xport
    def buzzer_set_frequency(self, frequency: int):
        self._buzz_client.buzzer_set_frequency(frequency)

    @_sync_xport
    def buzzer_get_frequency(self) -> int:
        return self._buzz_client.buzzer_get_frequency()

    @_sync_xport
    def buzzer_enable(self, on_time: int, off_time: int, repeat: int):
        self._buzz_client.buzzer_enable(on_time, off_time, repeat)

    @_sync_xport
    def buzzer_enable_ack(self):
        self._buzz_client.buzzer_enable_ACK()

    @_sync_xport
    def buzzer_enable_nak(self):
        self._buzz_client.buzzer_enable_NAK()

    # ===========
    # MDB METHODS
    # ===========

    @_sync_xport
    def mdb_execute_command(self, addr_cmd, txbuf, rxbuf):
        return self._mdb_client.mdb_execute_command(addr_cmd, txbuf, rxbuf)

    @_sync_xport
    def mdb_coin_changer_get_status(self) -> int:
        return self._mdb_client.mdb_coin_changer_get_status()

    @_sync_xport
    def mdb_coin_changer_get_setup_data(self):
        data = erpc.Reference()
        self._mdb_client.mdb_coin_changer_get_setup_data(data)
        data = data.value
        return dict(feature_level=data.feature_level,
                    currency_code=data.currency_code,
                    scaling_factor=data.scaling_factor,
                    decimal_places=data.decimal_places,
                    coin_routing=data.coin_routing,
                    coin_credits=data.coin_credits)

    @_sync_xport
    def mdb_coin_changer_get_expansion_data(self):
        data = erpc.Reference()
        self._mdb_client.mdb_coin_changer_get_expansion_data(data)
        data = data.value
        return dict(manufacturer_code=data.manufacturer_code,
                    serial_no=data.serial_no,
                    model_no=data.model_no,
                    software_ver=data.software_ver,
                    optional_features=data.optional_features)

    @_sync_xport
    def mdb_coin_changer_get_diagnostic_status(self):
        status = erpc.Reference()
        self._mdb_client.mdb_coin_changer_get_diagnostic_status(status)
        return status.value

    @_sync_xport
    def mdb_coin_changer_tube_status(self):
        full = erpc.Reference()
        status = erpc.Reference()
        err = self._mdb_client.mdb_coin_changer_tube_status(full, status)
        if err < 0:
            raise RuntimeWarning('failed to execute MDB command')
        return full.value, status.value

    @_sync_xport
    def mdb_coin_changer_coin_type(self, coin_enable, dispense_enable):
        err = self._mdb_client.mdb_coin_changer_coin_type(coin_enable, dispense_enable)
        if err < 0:
            raise RuntimeWarning('failed to execute MDB command')

    @_sync_xport
    def mdb_coin_changer_dispense(self, typ, cnt):
        err = self._mdb_client.mdb_coin_changer_dispense(typ, cnt)
        if err < 0:
            raise RuntimeWarning('failed to execute MDB command')

    @_sync_xport
    def mdb_coin_changer_expansion_feature_enable(self, feature_mask):
        err = self._mdb_client.mdb_coin_changer_expansion_feature_enable(feature_mask)
        if err < 0:
            raise RuntimeWarning('failed to execute MDB command')

    @_sync_xport
    def mdb_coin_changer_expansion_payout(self, value):
        err = self._mdb_client.mdb_coin_changer_expansion_payout(value)
        if err < 0:
            raise RuntimeWarning('failed to execute MDB command')

    @_sync_xport
    def mdb_coin_changer_expansion_payout_status(self):
        status = erpc.Reference()
        err = self._mdb_client.mdb_coin_changer_expansion_payout_status(status)
        if err < 0:
            raise RuntimeWarning('failed to execute MDB command')
        return status.value

    @_sync_xport
    def mdb_coin_changer_expansion_payout_poll(self):
        value = erpc.Reference()
        err = self._mdb_client.mdb_coin_changer_expansion_payout_poll(value)
        if err < 0:
            raise RuntimeWarning('failed to execute MDB command')
        elif err == 1:
            return value.value
        else:
            return None

    @_sync_xport
    def mdb_coin_changer_expansion_send_controlled_manual_fill_report(self):
        buf = erpc.Reference()
        err = self._mdb_client.mdb_coin_changer_expansion_send_controlled_manual_fill_report(buf)
        if err < 0:
            raise RuntimeWarning('failed to execute MDB command')
        return buf.value

    @_sync_xport
    def mdb_coin_changer_expansion_send_controlled_manual_payout_report(self):
        buf = erpc.Reference()
        err = self._mdb_client.mdb_coin_changer_expansion_send_controlled_manual_payout_report(buf)
        if err < 0:
            raise RuntimeWarning('failed to execute MDB command')
        return buf.value
