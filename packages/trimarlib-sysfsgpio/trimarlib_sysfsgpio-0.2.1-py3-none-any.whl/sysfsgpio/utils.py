import logging
import os
import sys
import threading

import pkg_resources

_logger = logging.getLogger('sysfsgpio.utils')


def pin2name(id: int) -> str:
    """Convert pin number to name"""
    if not isinstance(id, int):
        raise TypeError('id must be a non-negative integer')
    if id < 0:
        raise ValueError('id must be a non-negative integer')
    ports = 'ABCDEFGHIJKL'
    port_num = id // 32
    pin_num = id - (port_num * 32)
    if pin_num >= 32:
        raise ValueError('id out of range')
    try:
        return 'P{}{}'.format(ports[port_num], pin_num)
    except IndexError:
        raise ValueError('id out of range')


def name2pin(name: str) -> int:
    """Convert pin name to number"""
    if not isinstance(name, str):
        raise TypeError('name must be a string')
    if len(name) < 3:
        raise ValueError('invalid name format')
    name = name.upper()
    if name[0] != 'P':
        raise ValueError('invalid name format')
    ports = 'ABCDEFGHIJKL'
    port_idx = ports.find(name[1])
    if port_idx < 0:
        raise ValueError('port name out of range')
    return int(port_idx * 32 + int(name[2:]))


def get_pins() -> list:
    """Get pins available in the system

    :returns: a list whose entries are tuples in format (id, name)
    :rtype: list[tuple(int, str)]
    """
    pins = []
    try:
        entries = os.listdir('/sys/class/gpio')
    except FileNotFoundError:
        return pins
    _logger.debug('there are %d entries in /sys/class/gpio: %s', len(entries), entries)
    for e in entries:
        if e.startswith('gpiochip'):
            _logger.debug('ignoring chip device: %s', e)
        elif not e.startswith('gpio'):
            _logger.debug('ignoring non-pin entry: %s', e)
        else:
            try:
                idx = int(e[4:])
                name = pin2name(idx)
                pins.append((idx, name))
            except ValueError:
                _logger.exception('failed to parse: %s', e, exc_info=False)
                continue
    return pins


class Event(object):
    """Wrapper around a list of callbacks

    This class overloads operators for convenient manipulation of
    handlers. After initialization the internal handlers list is empty,
    callbacks may be added and removed using incremental
    addition/subtraction operators ('+=' and '-='). Adding already
    registered handler has no effect. Handlers list is internally
    protected with a lock, therefore this class is thread-safe. The
    class overloads __call__ method as well - calling an instance
    invokes all registered callbacks, handling any exceptions raised
    from within.
    """

    def __init__(self):
        self._handlers = []
        self._lock = threading.Lock()

    def __call__(self, *args, **kwargs):
        """Invoke all registered handlers passing positional and keyword arguments"""
        with self._lock:
            for hdlr in self._handlers:
                try:
                    hdlr(*args, **kwargs)
                except Exception:
                    _logger.exception('caught from handler: %s', hdlr)
        return

    def __iadd__(self, other):
        """Append callable object to handlers list

        :param other: callback object to register
        :type other: callable
        :raises TypeError: if object is not callable
        """

        self.append(other)
        return self

    def __isub__(self, other):
        """Remove object from the list. Has no effect if object has not been registered."""
        try:
            self.remove(other)
        except ValueError:
            pass
        return self

    def __len__(self):
        """Return length of the handlers list (count of registered callable objects)"""
        return self.count

    def append(self, other):
        """Append callable object to handlers list

        :param other: callback object to register
        :type other: callable
        :raises TypeError: if object is not callable
        """

        if not callable(other):
            raise TypeError('object must be callable')
        with self._lock:
            if other not in self._handlers:
                self._handlers.append(other)

    def remove(self, other):
        """Remove object from the list of handlers"""
        with self._lock:
            self._handlers.remove(other)

    def clear(self):
        """Remove all registered handlers"""
        with self._lock:
            self._handlers.clear()

    @property
    def count(self):
        """Return number of registered handlers"""
        return len(self._handlers)


def install_service():
    if not sys.platform.startswith('linux'):
        logging.error('platform not supported')
        return

    if '--force' in sys.argv:
        mode = 'w'
    else:
        mode = 'x'

    service_data = pkg_resources.resource_string('sysfsgpio', 'resources/gpio-exporter.service').decode()
    try:
        with open('/etc/systemd/system/gpio-exporter.service', mode) as fd:
            fd.write(service_data)
        os.system('systemctl daemon-reload')
        os.system('systemctl enable gpio-exporter')
        print('gpio-exporter service installed and enabled')
    except FileExistsError:
        print('ERROR: systemd service file already exists, use "--force" switch to overwrite')
    except PermissionError:
        print('ERROR: failed to open systemd service file - access denied, try running as super-user')


def install_rules():
    if not sys.platform.startswith('linux'):
        logging.error('platform not supported')
        return

    if '--force' in sys.argv:
        mode = 'w'
    else:
        mode = 'x'

    rules_data = pkg_resources.resource_string('sysfsgpio', 'resources/sysfsgpio.rules').decode()
    try:
        with open('/etc/udev/rules.d/99-sysfsgpio.rules', mode) as fd:
            fd.write(rules_data)
        os.system('udevadm control --reload-rules')
        os.system('udevadm trigger')
        print('sysfsgpio rules installed')
    except FileExistsError:
        print('ERROR: udev rules file already exists, use "--force" switch to overwrite')
    except PermissionError:
        print('ERROR: failed to open udev rules file - access denied, try running as super-user')


def install():
    if not sys.platform.startswith('linux'):
        logging.error('platform not supported')
        return

    install_service()
    install_rules()
