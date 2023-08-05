from LRC.Common.logger import logger
from LRC.Common.Exceptions import ArgumentError
from LRC.Controller.LRCKeySettings import KeySettings
import json

class AlternateKey(object):

    def __init__(self, enable, is_left=True):
        self.enable = enable # True or False
        self.is_left = is_left # True or False


class Controller(object):
    '''Controller for a key combination

    components:
        name:       Name of this combination
        ctrl:       Information of control key
        shift:      Information of shift key
        alt:        Information of alt key
        key:        The key to press for this Control

    '''

    settings = KeySettings('win32')

    class UnsupportedKeyForControllerError(Exception):

        def __init__(self, key, info=None):
            self.key = key
            self.info = info

        def __str__(self):
            if self.info:
                return 'un-supported key "{0}" for Controller : {1}.'.format(self.key, self.info)
            else:
                return 'un-supported key "{0}" for Controller.'.format(self.key)

    def __init__(self, name, *args, from_str=None, from_dump=None):
        self.name  = name

        self.ctrl  = AlternateKey(enable=False, is_left=True)
        self.shift = AlternateKey(enable=False, is_left=True)
        self.alt   = AlternateKey(enable=False, is_left=True)

        self.key = None

        keys = []
        keys.extend(args)

        if from_str:
            formatted = json.loads(from_str)
            if 1 != len(formatted):
                raise ValueError('Controller : Only one value should exist for parse : {}'.format(from_str))
            for v in formatted.values():
                keys.extend(v)

        if from_dump:
            if from_str:
                logger.warning('Controller : from_str will be overwritten by from_dump')
            if 1 != len(from_dump):
                raise ValueError('Controller : Only one value should exist for parse : {}'.format(from_dump))
            for v in from_dump.values():
                keys.extend(v)

        buffer = []
        for val in keys:
            buffer.append(val)

        for ctrl_tag in Controller.settings.ctrl_keys:
            if ctrl_tag in buffer:
                self.ctrl.enable = True
                self.ctrl.is_left = False if 'right' in ctrl_tag else True
                buffer.remove(ctrl_tag)

        for shift_tag in Controller.settings.shift_keys:
            if shift_tag in buffer:
                self.shift.enable = True
                self.shift.is_left = False if 'right' in shift_tag else True
                buffer.remove(shift_tag)

        for alt_tag in Controller.settings.alt_keys:
            if alt_tag in buffer:
                self.alt.enable = True
                self.alt.is_left = False if 'right' in alt_tag else True
                buffer.remove(alt_tag)

        n_left = len(buffer)
        if 1 == n_left:
            key = buffer[0]
            Controller.validate_key(key)
            self.key = key
        elif 0 == n_left: # 0 == n_left
            self.key = None
        else: # n_left > 1
            raise ArgumentError('Controller : un-recognized key(s), only one letter key needed, multiple provided : {0}'.format(keys) )

    def __str__(self):
        return self.dump_to_str()

    def dump_to_str(self):
        '''
        dump controller into string
        :return str:    string from controller
        '''
        return json.dumps(self.dump())

    def dump(self):
        '''
        dump controller into dictionary
        :return v:      a dict contains controller's name as key, and controller's keys(keyboard) as value
        '''
        buttons = []
        if self.ctrl.enable:
            if self.ctrl.is_left:
                buttons.append(Controller.settings.ctrl_keys[1])
            else:
                buttons.append(Controller.settings.ctrl_keys[2])
        if self.shift.enable:
            if self.shift.is_left:
                buttons.append(Controller.settings.shift_keys[1])
            else:
                buttons.append(Controller.settings.shift_keys[2])
        if self.alt.enable:
            if self.alt.is_left:
                buttons.append(Controller.settings.alt_keys[1])
            else:
                buttons.append(Controller.settings.alt_keys[2])
        if self.key:
            buttons.append(self.key)
        return { self.name : buttons }

    def get_key_list(self):
        key_list = []
        if self.ctrl.enable:
            if self.ctrl.is_left:
                key_list.append(self.settings.key_map['left ctrl'])
            else:
                key_list.append(self.settings.key_map['right ctrl'])
        if self.shift.enable:
            if self.shift.is_left:
                key_list.append(self.settings.key_map['left shift'])
            else:
                key_list.append(self.settings.key_map['right shift'])
        if self.alt.enable:
            if self.alt.is_left:
                key_list.append(self.settings.key_map['left alt'])
            else:
                key_list.append(self.settings.key_map['right alt'])
        if self.key:
            key_list.append(self.key)
        return key_list

    @staticmethod
    def validate_key(key):
        N = len(key)
        if key in Controller.settings.allowed_special_keys:
            return
        elif 1 == N: # letter or number
            if key.isalnum():
                return
            else:
                raise Controller.UnsupportedKeyForControllerError(key, 'expecting a letter or a number string length of 1 as a key')
        else:
            raise Controller.UnsupportedKeyForControllerError(key, 'un-supported special key')

    def available(self):
        if self.key:
            return True
        else:
            return False


class ControllerSet(object):
    '''Controller Collection(Use set as short for collection)

    components:
        name:           Name of this controller collection
        controllers:    Controllers(Controller) of this collection

    '''

    def __init__(self, name, from_str=None, from_dump=None, **kwargs):
        self.name = name
        self.controllers = {}
        logger.info('Collection: New Controller Set : {0}'.format(self.name))

        if from_str:
            formatted = json.loads(from_str)
            if 1 != len(formatted):
                raise ValueError('ControllerSet : Only one value should exist for parse : {}'.format(from_str))
            for v in formatted.values():
                kwargs.update(v)

        if from_dump:
            if from_str:
                logger.warning('ControllerSet : from_str will be overwritten by from_dump')
            if 1 != len(from_dump):
                raise ValueError('ControllerSet : Only one value should exist for parse : {}'.format(from_str))
            for v in from_dump.values():
                kwargs.update(v)

        for name, config in kwargs.items():
            logger.info('Collection:     {0} : {1}'.format(name, config))
            self.controllers[name] = (Controller(name, *config))

    def __str__(self):
        return self.dump_to_str()

    def dump(self):
        '''
        dump controller set(/collection) into a dictionary
        :return v:      dict with controller set name as key, controllers dicts as value
        '''
        controllers = {}
        for _, controller in self.controllers.items():
            controllers.update( controller.dump() )
        return { self.name : controllers }

    def dump_to_file(self, file_path):
        '''
        dump controller set into a file
        :param file_path:   where to dump
        :return:
        '''
        with open(file_path, 'w') as fh:
            fh.write(self.dump_to_str())

    def dump_to_str(self):
        '''
        dump controller set into a string
        :return str:
        '''
        return json.dumps(self.dump())

    def add_controller(self, controller):
        logger.info('Collection: Added to {0}(ControllerSet) : {1}'.format(self.name, controller.dump()))
        self.controllers[controller.name] = controller

    def remove_controller(self, controller):
        del(self.controllers[controller.name])
        logger.info('Collection: Remove from {0}(ControllerSet) : {1}'.format(self.name, controller.dump()))


class ControllerPackage(object):
    '''Controller Package : a collection of controller collections

    '''

    def __int__(self):
        pass


if '__main__' == __name__:
    a = Controller('test a', 'j', 'shift')
    b = Controller('test a', 'L', 'alt')
    a_str = str(a); b_str = str(b)

    c = Controller('aa', from_str=str(a))
    d = Controller('bb', from_str=str(b))

    e = Controller('aaa', from_dump=a.dump())
    f = Controller('bbb', from_dump=b.dump())

    print('controller a : {}'.format(a))
    print('controller b : {}'.format(b))
    print('controller c : {}'.format(c))
    print('controller d : {}'.format(d))
    print('controller e : {}'.format(e))
    print('controller f : {}'.format(f))

    s = ControllerSet('emmmm')
    s.add_controller(a)
    s.add_controller(b)

    sc = ControllerSet('copy str', from_str=str(s))
    sd = ControllerSet('copy dump', from_dump=s.dump())

    print('controller set s : {}'.format(s))
    print('controller set sc : {}'.format(sc))
    print('controller set sd : {}'.format(sd))



