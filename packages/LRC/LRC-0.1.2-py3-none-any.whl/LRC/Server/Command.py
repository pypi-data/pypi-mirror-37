from __future__ import print_function

class BaseCommand(object):

    def execute(self, **_kwargs):
        pass

class Command(BaseCommand):

    def __init__(self, name, execute, *, args=None, kwargs=None, **_kwargs):
        self.name = name
        self._execute_handler = execute
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return  '<{} :: {} :: {} :: {}>'.format(self.name, self._execute_handler, self.args, self.kwargs)

    def execute(self, *args, **kwargs):
        if self.args is not None and self.kwargs is not None:
            if args:
                _args = list(self.args)
                _args.extend(args)
            else:
                _args = self.args
            if kwargs:
                _kwargs = self.kwargs.copy()
                _kwargs.update(kwargs)
            else:
                _kwargs = self.kwargs
            self._execute_handler(*_args, **_kwargs)
        elif self.args is not None and self.kwargs is None:
            if args:
                _args = list(self.args)
                _args.extend(args)
            else:
                _args = self.args
            if kwargs:
                raise ValueError('execute handler do not support kwargs')
            self._execute_handler(*_args)
        elif self.args is None and self.kwargs is not None:
            if args:
                raise ValueError('execute handler do not support args')
            if kwargs:
                _kwargs = self.kwargs.copy()
                _kwargs.update(kwargs)
            else:
                _kwargs = self.kwargs
            self._execute_handler(**_kwargs)
        else: # self.args is None and self.kwargs is None
            if args or kwargs:
                raise ValueError('execute handler do not support args and kwargs')
            self._execute_handler()


def _get_full_interface(module, interface):
    if interface.startswith(module):
        return interface
    else:
        return module + '.' + interface


def parse_command(**_kwargs):
    '''
    parse one command from settings
    :param **kwargs:    setting for command
    :return command:    command parsed from settings
    available settings :
        import      -- the module will import
        kwargs      -- parameters for command execution
        execute     -- attribute of module, used as execute handler for common command (LRC.Server.Command.Command)
        command     -- command class
    '''
    if 'import' in _kwargs:
        module = _kwargs['import']
        exec('import ' + module)
        del _kwargs['import']
    else:
        module = ''

    args = list()
    if 'interface' in _kwargs or 'command' in _kwargs:
        if 'args' in _kwargs:
            args = _kwargs['args']
            del _kwargs['args']

    if 'interface' in _kwargs: # interface to get command instance
        interface = _get_full_interface(module, _kwargs['interface'])
        del _kwargs['interface']
        if args:
            return eval(interface)(*args, **_kwargs)
        else:
            return eval(interface)(**_kwargs)

    if 'command' in _kwargs: # command class
        command_class = _get_full_interface(module, _kwargs['command'])
        del _kwargs['command']
        if args:
            return eval(command_class)(*args, **_kwargs)
        else:
            return eval(command_class)(**_kwargs)

    if 'execute_interface' in _kwargs: # interface to get execute handler for a common command (LRC.Server.Command.Command)
        execute_interface = _get_full_interface(module, _kwargs['execute_interface'])
        del _kwargs['execute_interface']
        return Command(name="parsed from string", execute=eval(execute_interface)(), **_kwargs)

    if 'execute' in _kwargs: # execute handler for a common command (LRC.Server.Command.Command)
        execute = _get_full_interface(module, _kwargs['execute'])
        del _kwargs['execute']
        return Command(name="parsed from string", execute=eval(execute), **_kwargs)

    raise ValueError('parse_command : one of the following should be specified : {}'.format(
            {'interface','command','execute_interface','execute'}))


if '__main__' == __name__:

    def __test_case_000(): # test directly parse from config
        command_config={'import':'LRC.Server.Commands.CommandTest', 'interface':'get_command_instance'}
        command = parse_command(**command_config)
        print(command)
        command.execute()

    def __test_case_001(): # test parse from json file
        import os, json
        config_file = os.path.join('LRC','Server','commands_test.json')
        with open(config_file, 'r') as fh:
            config_content = fh.read()
        commands_config = json.loads(config_content)
        commands = dict()
        for name, body in commands_config.items():
            print('registering command {} with {}'.format(name, body))
            commands[name] = parse_command(**body)
        for name, command in commands.items():
            print('executing command {}'.format(name))
            command.execute()

    def __test_case_002(): # test directly parse from config with args (just parse, the command do not work)
        command_config={
            'import':'Test.T009_pack_and_unpack',
            'interface':'target',
            'name':'top level name', # <top level name> you'll need me later
            'value':'top level value', # <top level value> you'll need me later
            'args':['may be portal', 'another trial', 'Lannister always pay'],
            'kwargs':{ # kwargs is reserved for command parse process
                'name':'test', # the value of kwargs will pass to **kwargs as keyword "kwargs"
                'value':'joke', # if just k-v pair need to pass to interface, just do as <top level name/value> above
            'what\'s left':'all here for rot',
            },
        }
        parse_command(**command_config)


    __test_case_002()