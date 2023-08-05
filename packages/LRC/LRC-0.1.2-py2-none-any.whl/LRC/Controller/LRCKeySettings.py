from LRC.Controller.win32keydefines import *
from LRC.Common.Exceptions import ArgumentError
import sys

class KeyCombinationNotAvailableError(ArgumentError):

    def __init__(self, *args):
        self.keys = []
        for k in args:
            self.keys.append(k)

    def __str__(self):
        n = len(self.keys)
        if 0 == n:
            return ('Key combination not available : no key found')
        elif 1 == n:
            return ('Key combination not available : {0}'.format(self.keys[0]))
        elif 2 == n:
            return ('Key combination not available : {0}, {1}'.format(self.keys[0], self.keys[1]))
        elif 3 == n:
            return ('Key combination not available : {0}, {1}, {2}'.format(self.keys[0], self.keys[1], self.keys[2] ))
        else:
            return ('Key combination not available : {0}, {1}, {2}, ...'.format(self.keys[0], self.keys[1], self.keys[2] ))


class KeySettings(object):
    '''Key Settings for LAN Remote Controller

    components:
        ctrl_keys:              keys for 'ctrl'
        shift_keys:             keys for
        alt_keys:
        allowed_special_keys:   Special keys allows, i.e. 'space', 'left arrow'
        key_map:
    '''

    def __init__(self, platform=None):
        if platform:
            if platform.startswith('java'):
                raise NotImplementedError()
                # from .java_ import PyKeyboard
            elif platform == 'darwin':
                raise NotImplementedError()
                # from .mac import PyKeyboard, PyKeyboardEvent
            elif platform == 'win32':
                self._init_windows_setting()
            else:
                raise NotImplementedError()
        else:
            if sys.platform.startswith('java'):
                raise NotImplementedError()
                # from .java_ import PyKeyboard
            elif sys.platform == 'darwin':
                raise NotImplementedError()
                # from .mac import PyKeyboard, PyKeyboardEvent
            elif sys.platform == 'win32':
                self._init_windows_setting()
            else:
                raise NotImplementedError()
                # from .x11 import PyKeyboard, PyKeyboardEvent

    def _init_windows_setting(self):

        self.ctrl_keys  = ['ctrl',  'left ctrl',  'right ctrl', ] # control
        self.shift_keys = ['shift', 'left shift', 'right shift',] # shift
        self.alt_keys   = ['alt',   'left alt',    'right alt',  ] # alt

        self.allowed_special_keys = [
            'left arrow', 'right arrow', 'up arrow', 'down arrow',
            'space', 'home', 'end',
        ]

        self.key_map = {
            # functional key
            'ctrl':          VK_CONTROL,
            'left ctrl':    VK_LCONTROL,
            'right ctrl':   VK_RCONTROL,
            'alt':           VK_LMENU,
            'left alt':      VK_LMENU,
            'right alt':     VK_RMENU,
            'shift':         VK_SHIFT,
            'left shift':    VK_LSHIFT,
            'right shift':   VK_RSHIFT,
            # arrow key
            'left arrow':   VK_LEFT,
            'right arrow':  VK_RIGHT,
            'up arrow':     VK_UP,
            'down arrow':   VK_DOWN,
            # other
            'space':        VK_SPACE,
            'home':         VK_HOME,
            'end':          VK_END,
        }




