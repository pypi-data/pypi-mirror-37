import logging
import os
import select
import threading
import time

from .utils import Event, pin2name, name2pin


class Pin(object):
    """Utility wrapper around sysfs GPIO interface."""

    def __init__(self, pin, direction: str = 'in', invert: bool = None, *, logger: logging.Logger = None):
        """Initialize Pin object

        :param pin: name or number of the pin
        :type pin: str or int
        :param str direction: initial direction of the pin, accepted values are 'in' and 'out', defaults to 'in'
        :param bool invert: flag indicating whether to use inverted logic, defaults to None which means no change
        :param logging.Logger logger: logger instance to use
        :raises ValueError: if failed to decode pin name
        :raises TypeError: if supplied parameter is neither an integer nor a string
        :raises FileNotFoundError: if specified pin is not available
        """

        self._thread = None
        self._thread_lock = threading.Lock()
        self._thread_cancel = threading.Event()
        self._input_changed = Event()
        self._logger = logger or logging.getLogger('sysfsgpio.Pin')
        self._event = threading.Event()

        self._config = dict(debounce=.1, ontime=-1.0, offtime=-1.0, repeat=-1, pattern=[])

        if isinstance(pin, int):
            self._pinname = pin2name(pin)
            self._pin = pin
        elif isinstance(pin, str):
            try:
                self._pin = name2pin(pin)
                self._pinname = pin
            except ValueError:
                pin = int(pin)
                self._pinname = pin2name(pin)
                self._pin = pin
        else:
            raise TypeError('pin must be an integer, a valid pin name or a string convertible to integer')

        self._path = '/sys/class/gpio/gpio{:d}'.format(self._pin)

        if direction is not None:
            if type(direction) is not str:
                raise TypeError('direction: expected str, got {}'.format(type(direction)))
            if direction not in ['in', 'out']:
                raise ValueError('direction: expecting "in" or "out"')
            with open(os.path.join(self._path, 'direction'), 'w') as fd:
                fd.write(direction)
        if invert is not None:
            if type(invert) is not bool:
                raise TypeError('invert: expected bool, got {}'.format(type(invert)))
            with open(os.path.join(self._path, 'active_low'), 'w') as fd:
                fd.write(str(int(invert)))

        try:
            os.stat(os.path.join(self._path, 'edge'))
            with open(os.path.join(self._path, 'edge'), 'w') as fd:
                fd.write('none')
        except FileNotFoundError:
            self._logger.warning('pin %s does not support interrupts', self.pinname)
        return

    def _thread_start(self):
        if self.direction == 'in':
            target = self._input_fun
            name = 'gpio{}-input'.format(self._pin)
        else:
            target = self._output_fun
            name = 'gpio{}-output'.format(self._pin)
        self._thread = threading.Thread(target=target, name=name)
        self._thread.start()

    def _thread_stop(self):
        self._thread_cancel.set()
        self._thread.join()
        self._thread = None
        self._thread_cancel.clear()

    @property
    def pin(self):
        """Return pin number"""
        return self._pin

    @property
    def pinname(self):
        """Return pin name"""
        return self._pinname

    def register_callback(self, callback):
        """Append callback to the list

        :param callback: callback object to register, will be invoked with two positional arguments: sender (Pin object,
                         origin of the event) and value (new state of the pin)
        :type callback: callable
        """
        self._input_changed += callback

    def unregister_callback(self, callback):
        """Remove previously registered callback object from the list

        :param callback: callback object to unregister
        :type callback: callable
        """
        self._input_changed -= callback

    def clear_callbacks(self):
        """Remove all callback objects registered for the pin"""
        self._input_changed.clear()

    def get_value(self) -> int:
        """Read current state of the pin
        
        :return: value of the pin
        :rtype: int
        """
        with open(os.path.join(self._path, 'value'), 'r') as fd:
            return int(fd.read())

    def set_value(self, value):
        """Set value of the pin

        :param value: value to be set
        :type value: int or str or bool
        :raises RuntimeError: if worker thread is alive
        """
        with self._thread_lock:
            if self._thread is not None and self._thread.is_alive():
                raise RuntimeError('worker thread running')
            with open(os.path.join(self._path, 'value'), 'w') as fd:
                fd.write(str(int(value)))

    def get_invert(self) -> bool:
        """Read flag indication logic inversion
        
        :return: flag indicating whether pin logic is inverted
        :rtype: bool
        """
        with open(os.path.join(self._path, 'active_low'), 'r') as fd:
            return bool(int(fd.read()))

    def set_invert(self, invert: bool):
        """Set logic inversion
        
        :param bool invert: True to use inverted logic, False otherwise
        """
        with open(os.path.join(self._path, 'active_low'), 'w') as fd:
            fd.write(str(int(invert)))

    def get_direction(self) -> str:
        """Get pin direction
        
        :return: pin direction, 'in' or 'out'
        :rtype: str
        """
        with open(os.path.join(self._path, 'direction'), 'r') as fd:
            return fd.read().strip()

    def set_direction(self, direction: str):
        """Set pin direction

        Changing pin direction immediately disables worker thread.

        :param str direction: pin direction, accepted values are 'in' and 'out'
        :raises TypeError: if direction is not a string
        :raises ValueError: if direction is not in accepted range
        """
        if not isinstance(direction, str):
            raise TypeError('direction must be a string')
        if direction not in ['in', 'out']:
            raise ValueError('invalid direction value')
        with self._thread_lock:
            if direction == self.get_direction():
                return
            if self._thread is not None:
                self._logger.info('stopping worker thread due to direction change')
                self._thread_stop()

            with open(os.path.join(self._path, 'direction'), 'w') as fd:
                fd.write(direction)

    def get_enabled(self) -> bool:
        """Get state of the worker thread

        :return: flag indicating whther worker thread is running
        :rtype: bool
        """
        with self._thread_lock:
            return self._thread is not None and self._thread.is_alive()

    def enable(self):
        """Start worker thread if not already running"""
        with self._thread_lock:
            if self._thread is not None:
                if self._thread.is_alive():
                    return
                self._thread_stop()
            self._thread_start()

    def disable(self):
        """Stop worker thread"""
        with self._thread_lock:
            if self._thread is None:
                return
            self._thread_stop()

    def set_enabled(self, enabled: bool):
        """Set state of the worker thread
        
        :param bool enabled: True to start worker thread, False to stop it
        """
        if not isinstance(enabled, bool):
            raise TypeError('enabled must be a boolean')
        if enabled:
            self.enable()
        else:
            self.disable()

    start = enable
    stop = disable

    def get_debounce(self) -> float:
        """Get input debounce time
        
        :return: input debounce time
        :rtype: float
        """
        return self._config['debounce']

    def set_debounce(self, debounce: float):
        """Set input debounce time

        :param float debounce: debounce time, i.e. time (in seconds) for which input has to be
                               in steady state before its value is latched
        """
        self._config['debounce'] = float(debounce)

    def get_ontime(self) -> float:
        """Get output on time
        
        :return: output on time
        :rtype: float
        """
        return self._config['ontime']

    def set_ontime(self, ontime: float):
        """Set output on time

        :param float ontime: input on time
        """
        self._config['ontime'] = float(ontime)

    def get_offtime(self) -> float:
        """Get output off time
        
        :return: output off time
        :rtype: float
        """
        return self._config['offtime']

    def set_offtime(self, offtime: float):
        """Set output off time

        :param float offtime: output off time
        """
        self._config['offtime'] = float(offtime)

    def get_repeat(self) -> int:
        """Get output cycle repetition count
        
        :return: output repetition count
        :rtype: int
        """
        return self._config['repeat']

    def set_repeat(self, repeat: int):
        """Set output cycle repetition count

        :param int repeat: output cycle repetition count, negative values indicate infinite count
        """
        self._config['repeat'] = int(repeat)

    def get_pattern(self) -> list:
        """Get output transitions pattern

        :return: output transitions pattern
        :rtype: list[float]
        """
        return self._config['pattern'].copy()

    def set_pattern(self, value: list):
        """Set output transitions pattern

        :param value: list of delays between output transitions
        :type value: list[float]
        """
        pattern = []
        for v in value:
            vv = float(v)
            if vv < 0:
                raise ValueError('pattern must consist of non-negative values')
            pattern.append(vv)
        self._config['pattern'] = pattern

    def get_configuration(self):
        """Get pin configuration

        Returns a dictionary representing current pin configuration. Keys of that 
        dictionary refer to the properties of the object, they are as follows:
        - direction,
        - invert,
        - debounce,
        - ontime,
        - offtime,
        - repeat,
        - pattern.
        This method (and matching setter) acts as a convenience wrapper.

        :return: configuration dictionary
        :rtype: dict
        """
        return dict(
            direction=self.get_direction(),
            invert=self.get_invert(),
            debounce=self.get_debounce(),
            ontime=self.get_ontime(),
            offtime=self.get_offtime(),
            repeat=self.get_repeat(),
            pattern=self.get_pattern()
        )

    def set_configuration(self, config: dict = None, *,
                          direction: str = None,
                          invert: bool = None,
                          debounce: float = None,
                          ontime: float = None,
                          offtime: float = None,
                          repeat: int = None,
                          pattern: list = None):
        """Set pin configuration

        This method acts as a convenience wrapper and enables configuring multiple properties at once.

        :param dict config: configuration dictionary
        :param str direction: pin direction, 'in' or 'out'
        :param bool invert: pin logic inversion flag
        :param float debounce: input debounce time
        :param float ontime: output on time
        :param float offtime: output off time
        :param int repeat: output repetition count
        :param list pattern: list of delay between output transitions
        """
        todo = []
        if direction is not None or 'direction' in config:
            todo.append((self.set_direction, direction or config['direction']))
        if invert is not None or 'invert' in config:
            todo.append((self.set_invert, invert or config['invert']))
        if debounce is not None or 'debounce' in config:
            todo.append((self.set_debounce, debounce or config['debounce']))
        if ontime is not None or 'ontime' in config:
            todo.append((self.set_ontime, ontime or config['ontime']))
        if offtime is not None or 'offtime' in config:
            todo.append((self.set_offtime, offtime or config['offtime']))
        if repeat is not None or 'repeat' in config:
            todo.append((self.set_repeat, repeat or config['repeat']))
        if pattern is not None or 'pattern' in config:
            todo.append((self.set_pattern, pattern or config['pattern']))
        for setter, value in todo:
            setter(value)

    value = property(get_value, set_value)
    invert = property(get_invert, set_invert)
    direction = property(get_direction, set_direction)
    enabled = property(get_enabled, set_enabled)
    debounce = property(get_debounce, set_debounce)
    ontime = property(get_ontime, set_ontime)
    offtime = property(get_offtime, set_offtime)
    repeat = property(get_repeat, set_repeat)
    pattern = property(get_pattern, set_pattern)
    configuration = property(get_configuration, set_configuration)

    def _input_fun(self):
        cth = threading.current_thread()
        self._logger.info('%s started', cth.name)
        try:
            try:
                with open(os.path.join(self._path, 'edge'), 'w') as fd:
                    fd.write('both')
                poll = select.poll()
            except (FileNotFoundError, PermissionError):
                poll = None

            with open(os.path.join(self._path, 'value'), 'r') as fd:
                stamp = 0
                v = int(fd.read())
                vv = v
                fd.seek(0)

                if poll is not None:
                    poll.register(fd, select.POLLPRI)
                while not self._thread_cancel.is_set():
                    if poll is not None:
                        ret = poll.poll(self._config['debounce'] * 1000)
                        if len(ret) != 0:
                            vv = int(fd.read())
                            fd.seek(0)
                            continue
                    else:
                        if self._thread_cancel.wait((stamp + self._config['debounce']) - time.time()):
                            continue
                        vv = int(fd.read())
                        fd.seek(0)
                        stamp = time.time()
                    if v != vv:
                        v = vv
                        if len(self._input_changed) > 0:
                            self._input_changed(self, v)
                        else:
                            self._logger.info('%s, v=%s, no event handler installed', cth.name, v)
        except Exception:
            self._logger.exception('%s : input processing failed', cth.name)
        finally:
            try:
                with open(os.path.join(self._path, 'edge'), 'w') as fd:
                    fd.write('none')
            except (FileNotFoundError, PermissionError):
                pass
            except Exception:
                self._logger.exception('failed to disable interrupts')
        self._logger.info('%s returning', cth.name)
        return

    def _output_pattern_mode(self):
        pattern = self._config['pattern']
        with open(os.path.join(self._path, 'value'), 'r+') as fd:
            v = bool(int(fd.read()))
            fd.seek(0)
            # first toggle
            v = not v
            fd.write(''.join([str(int(v)), '\n']))
            fd.seek(0)
            for dly in pattern:
                if self._thread_cancel.wait(dly):
                    self._logger.info('thread cancelled')
                    break
                v = not v
                fd.write(''.join([str(int(v)), '\n']))
                fd.seek(0)
            else:
                self._logger.debug('pattern complete')
        return

    def _output_toggling_mode(self):
        remcnt = self._config['repeat']
        with open(os.path.join(self._path, 'value'), 'r+') as fd:
            v = bool(int(fd.read()))
            fd.seek(0)
            # first toggle
            v = not v
            fd.write(''.join([str(int(v)), '\n']))
            fd.seek(0)
            while remcnt != 0:
                if v:
                    dly = self._config['ontime']
                    if remcnt > 0:
                        remcnt -= 1
                    elif remcnt < 0 <= self._config['repeat']:
                        remcnt = self._config['repeat']
                else:
                    dly = self._config['offtime']
                if dly < 0:
                    self._logger.info('steady state detected')
                    break
                if self._thread_cancel.wait(dly):
                    self._logger.info('thread cancelled')
                    break
                v = not v
                fd.write(''.join([str(int(v)), '\n']))
                fd.seek(0)
            else:
                self._logger.debug('toggling complete')
        return

    def _output_fun(self):
        cth = threading.current_thread()
        self._logger.info('%s started', cth.name)
        try:
            if len(self._config['pattern']) > 0:
                self._logger.debug('output in pattern mode')
                self._output_pattern_mode()
            else:
                self._logger.debug('output in toggling mode')
                self._output_toggling_mode()
        except Exception:
            self._logger.exception('%s: output processing failed', cth.name)
        self._logger.info('%s returning', cth.name)
        return
