import logging
import struct
import threading
import time
from functools import wraps

import erpc
import serial

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
                raise RuntimeError('device is not open!');
            return fn(self, *args, **kwargs)

    return _fn


class APSBackBone(object):
    def __init__(self, port='/dev/ttyS1', *, baudrate=115200, logger=None):
        self._logger = logger or logging.getLogger('.'.join(['apsbblib', 'APSBackBone']))
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
            self._pins['irq'].enabled = True
            self._pins['icom'].enabled = True
            self._pins['breach'].enabled = True

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
            if v == 0:
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
            elif not self._dispatcher_event.wait(0.5):
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
                        path_status = status.value
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
                    self._xport._serial.flushInput()
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
            self._dispatcher_thread.start()
        return

    def close(self):
        with self._xport_lock:
            if self._dispatcher_thread is None:
                return
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
    def barrier_event(self):
        return self._event_callbacks['barrier']

    @barrier_event.setter
    def barrier_event(self, value):
        with self._event_callbacks_lock:
            self._event_callbacks['barrier'] = value

    @property
    def vehicle_event(self):
        return self._event_callbacks['vehicle']

    @vehicle_event.setter
    def vehicle_event(self, value):
        with self._event_callbacks_lock:
            self._event_callbacks['vehicle'] = value

    @property
    def button_event(self):
        return self._event_callbacks['button']

    @button_event.setter
    def button_event(self, value):
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
    def btn_set_config(self, enable, invert):
        self._btn_client.btn_set_config(enable, invert)

    @_sync_xport
    def btn_get_config(self):
        enable = erpc.Reference()
        invert = erpc.Reference()
        self._btn_client.btn_get_config(enable, invert)
        return enable.value, invert.value

    @_sync_xport
    def rgb_set_colour(self, colour):
        self._rgb_client.rgb_set_colour(colour)

    @_sync_xport
    def rgb_get_colour(self):
        colour = erpc.Reference()
        self._rgb_client.rgb_get_colour(colour)
        return colour.value

    @_sync_xport
    def rgb_set_timings(self, timings):
        self._rgb_client.rgb_set_timings(timings)

    @_sync_xport
    def rgb_get_timings(self):
        timings = erpc.Reference()
        self._rgb_client.rgb_get_timings(timings)
        return timings.value

    @_sync_xport
    def rgb_set_mode(self, mode):
        self._rgb_client.rgb_set_mode(mode)

    @_sync_xport
    def rgb_get_mode(self):
        return self._rgb_client.rgb_get_mode()

    @_sync_xport
    def rgb_set_coefficients(self, coeffs):
        self._rgb_client.rgb_set_coefficients(coeffs)

    @_sync_xport
    def rgb_get_coefficients(self):
        coeffs = erpc.Reference()
        self._rgb_client.rgb_get_coefficients(coeffs)
        return coeffs.value

    @_sync_xport
    def rgb_set_config(self, mode, timings, colour, coeffs):
        self._rgb_client.rgb_set_config(mode, timings, colour, coeffs)

    @_sync_xport
    def rgb_get_config(self):
        mode = erpc.Reference()
        timings = erpc.Reference()
        colour = erpc.Reference()
        coeffs = erpc.Reference()
        self._rgb_client.rgb_get_config(mode, timings, colour, coeffs)
        return mode.value, timings.value, colour.value, coeffs.value

    @_sync_xport
    def path_get_status(self):
        status = erpc.Reference()
        self._path_client.path_get_status(status)
        return status.value

    @_sync_xport
    def path_open(self, force=False, auto_close=True):
        self._path_client.path_open(force, auto_close)

    @_sync_xport
    def path_close(self):
        self._path_client.path_close()

    @_sync_xport
    def path_set_barrier_timeout(self, timeout):
        self._path_client.path_set_barrier_timeout(timeout)

    @_sync_xport
    def path_get_barrier_timeout(self):
        return self._path_client.path_get_barrier_timeout()

    @_sync_xport
    def path_set_loops_timeout(self, timeout):
        self._path_client.path_set_loops_timeout(timeout)

    @_sync_xport
    def path_get_loops_timeout(self):
        return self._path_client.path_get_loops_timeout()

    @_sync_xport
    def path_set_loops_hold(self, time_ms):
        self._path_client.path_set_loops_hold(time_ms)

    @_sync_xport
    def path_get_loops_hold(self):
        return self._path_client.path_get_loops_hold()

    @_sync_xport
    def path_get_result(self):
        return self._path_client.path_get_result()

    @_sync_xport
    def path_clear_result(self):
        self._path_client.path_clear_result()

    @_sync_xport
    def path_set_config(self, barrier_timeout, loops_timeout, loops_hold):
        self._path_client.path_set_config(barrier_timeout,
                                          loops_timeout,
                                          loops_hold)

    @_sync_xport
    def path_get_config(self):
        barrier_timeout = erpc.Reference()
        loops_timeout = erpc.Reference()
        loops_hold = erpc.Reference()
        self._path_client.path_get_config(barrier_timeout,
                                          loops_timeout,
                                          loops_hold)
        return barrier_timeout.value, loops_timeout.value, loops_hold.value

    @_sync_xport
    def buzzer_set_frequency(self, frequency):
        self._buzz_client.buzzer_set_frequency(frequency)

    @_sync_xport
    def buzzer_get_frequency(self):
        return self._buzz_client.buzzer_get_frequency()

    @_sync_xport
    def buzzer_enable(self, on_time, off_time, repeat):
        self._buzz_client.buzzer_enable(on_time, off_time, repeat)

    @_sync_xport
    def buzzer_enable_ack(self):
        self._buzz_client.buzzer_enable_ACK()

    @_sync_xport
    def buzzer_enable_nak(self):
        self._buzz_client.buzzer_enable_NAK()

    @_sync_xport
    def mdb_execute_command(self, addr_cmd, txbuf, rxbuf):
        return self._mdb_client.mdb_execute_command(addr_cmd, txbuf, rxbuf)

    @_sync_xport
    def mdb_coin_changer_get_status(self):
        return self._mdb_client.mdb_coin_changer_get_status()

    @_sync_xport
    def mdb_coin_changer_get_setup_data(self):
        data = erpc.Reference()
        self._mdb_client.mdb_coin_changer_get_setup_data(data)
        return data.value

    @_sync_xport
    def mdb_coin_changer_get_expansion_data(self):
        data = erpc.Reference()
        self._mdb_client.mdb_coin_changer_get_expansion_data(data)
        return data.value

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
            raise RuntimeWarning()
        return full.value, status.value

    @_sync_xport
    def mdb_coin_changer_coin_type(self, coin_enable, dispense_enable):
        err = self._mdb_client.mdb_coin_changer_coin_type(coin_enable, dispense_enable)
        if err < 0:
            raise RuntimeWarning()

    @_sync_xport
    def mdb_coin_changer_dispense(self, typ, cnt):
        err = self._mdb_client.mdb_coin_changer_dispense(typ, cnt)
        if err < 0:
            raise RuntimeWarning()

    @_sync_xport
    def mdb_coin_changer_expansion_feature_enable(self, feature_mask):
        err = self._mdb_client.mdb_coin_changer_expansion_feature_enable(feature_mask)
        if err < 0:
            raise RuntimeWarning()

    @_sync_xport
    def mdb_coin_changer_expansion_payout(self, value):
        err = self._mdb_client.mdb_coin_changer_expansion_payout(value)
        if err < 0:
            raise RuntimeWarning()

    @_sync_xport
    def mdb_coin_changer_expansion_payout_status(self):
        status = erpc.Reference()
        err = self._mdb_client.mdb_coin_changer_expansion_payout_status(status)
        if err < 0:
            raise RuntimeWarning()
        return status.value

    @_sync_xport
    def mdb_coin_changer_expansion_payout_poll(self):
        value = erpc.Reference()
        err = self._mdb_client.mdb_coin_changer_expansion_payout_poll(value)
        if err < 0:
            raise RuntimeWarning()
        elif err == 1:
            return value.value
        else:
            return None

    @_sync_xport
    def mdb_coin_changer_expansion_send_controlled_manual_fill_report(self):
        buf = erpc.Reference()
        err = self._mdb_client.mdb_coin_changer_expansion_send_controlled_manual_fill_report(buf)
        if err < 0:
            raise RuntimeWarning()
        return buf.value

    @_sync_xport
    def mdb_coin_changer_expansion_send_controlled_manual_payout_report(self):
        buf = erpc.Reference()
        err = self._mdb_client.mdb_coin_changer_expansion_send_controlled_manual_payout_report(buf)
        if err < 0:
            raise RuntimeWarning()
        return buf.value
