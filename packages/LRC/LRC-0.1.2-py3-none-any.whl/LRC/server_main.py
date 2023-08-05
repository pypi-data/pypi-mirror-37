from __future__ import print_function
from LRC.Common.logger import logger

def main():
    import sys
    # parse config
    config, commands, commands_kwargs, reserved = parse_config_from_console_line(sys.argv[1:])
    # update system arguments to avoid kivy error
    sys.argv = sys.argv[0:1]
    sys.argv.extend(reserved)
    # start server
    start_lrc_server_main(config, commands, commands_kwargs)


def start_lrc_server_main(config, commands, commands_kwargs):

    if config.enable_ui:
        from multiprocessing import freeze_support
        from LRC.Server.ServerUI import LRCServerUI

        freeze_support()

        logger.set_logger(name='kivy')
        logger.flush_buffers()

        if commands:
            logger.warning('LRC : UI is enabled, commands {} will not be executed.'.format(commands))

        ui = LRCServerUI(**config.server_config)
        ui.run()
    else:
        from LRC.Server.CommandServer import CommandServer
        import sys

        logger.flush_buffers()

        # start a new command server if necessary
        command_server = CommandServer(**config.command_server_config)
        if command_server.is_running:
            _register_lrc_commands(command_server, config, commands_kwargs, register_remotely=True)
        else:
            command_server.start()
            _register_lrc_commands(command_server, config, commands_kwargs, register_remotely=False) # register after default command file loaded
        # send the command
        for cmd in commands:
            command_server.send_command(cmd, **commands_kwargs[cmd])


def parse_config_from_console_line(args):
    from LRC.Server.Config import LRCServerConfig
    from LRC.Common.empty import empty
    import re
    # init
    reserved = list()
    commands = list()
    n_commands = 0
    commands_kwargs = dict()
    config = LRCServerConfig()
    config_command_lines = dict()
    command_param_exp = re.compile(r'^(\w+)\=')
    verbose_info = empty

    # check some special flags
    if '--help' in args or '-h' in args:
        print(_help_commands())
        exit()
    if '--version' in args:
        from LRC.Common.info import version
        print('LRC version {}'.format(version))
        exit()

    # processed_flags contains all flags that have been processed before walk through all arguments
    processed_flags = []
    if '--verbose' in args:
        config_command_lines['verbose'] = True
        def _verbose_info(info):
            logger.buffer_info('LRC : verbose : {}'.format(info))
        verbose_info = _verbose_info
        verbose_info('--verbose given, enable verbose info')
        processed_flags.append('--verbose')
    if '--enable-ui' in args:
        config_command_lines['enable_ui'] = True
        verbose_info('--enable-ui given, enable server UI')
        processed_flags.append('--enable-ui')
    if '--no-ui' in args:
        config_command_lines['enable_ui'] = False
        verbose_info('--no-ui given, disable server UI')
        processed_flags.append('--no-ui')
    # check the rest of them
    commands_kwargs['default'] = dict()
    current_command = 'default'
    ix = 0 # console argument index
    while ix < len(args):
        arg = args[ix]
        if arg.startswith('--config-file='):
            config.config_file = arg[len('--config-file='):]
            verbose_info('--config-file given, loading config from file {}'.format(config.config_file))
            verbose_info('config loaded : {}'.format(config))
            processed_flags.append(arg)
        else:
            if arg.startswith('--'): # --xxx config flag
                if arg not in processed_flags:
                    reserved.append(arg)
            elif arg.startswith('-'):
                reserved.append(arg)
            else:
                tmp = command_param_exp.findall(arg) # kkk=vvv
                if len(tmp) > 0:
                    param_name = tmp[0]
                    param_value_str = arg[len(param_name)+1:]
                    try:
                        commands_kwargs[current_command][param_name] = eval(param_value_str)
                        verbose_info('add param "{}"({}) for command "{}"'.format(param_name, commands_kwargs[current_command][param_name], current_command))
                    except Exception as err:
                        logger.buffer_error('LRC : parse command parameter failed from {} : {}'.format(param_value_str, err.args))
                else:
                    commands.append(arg)
                    current_command = commands[n_commands]
                    commands_kwargs[current_command] = dict()
                    n_commands += 1
                    verbose_info('add command {}'.format(current_command))
        ix += 1
    # sync config with command line configurations
    config.apply_config(**config_command_lines)
    # clean up
    if 0 == len(commands) and not config.enable_ui:
        logger.buffer_info('LRC : no command given, start_lrc will be executed.')
        commands.append('start_lrc')
        commands_kwargs['start_lrc'] = dict()
        commands_kwargs['start_lrc'].update(**config.server_config)
        commands_kwargs['start_lrc'].update(**config.waiter_config)

    if 0 != len(reserved):
        msg = '\n'
        for flag in reserved:
            msg += '    {}\n'.format(flag)
        logger.buffer_warning('LRC : options will be passed to kivy framework : {}.'.format(msg))

    # for now, default command arguments are passed to command server
    config._update_command_server_config(**commands_kwargs['default'])

    return config, commands, commands_kwargs, reserved


def _register_lrc_commands(command_server, config, commands_kwargs, register_remotely=False):
    from LRC.Server.Commands.LRCServer import start_lrc, start_lrc_server, start_lrc_waiter
    from LRC.Server.Commands.LRCServer import stop_lrc, stop_lrc_server, stop_lrc_waiter
    from LRC.Server.Commands.LRCServer import quit as quit_lrc
    from LRC.Server.Command import Command

    remote_command_config = dict()

    # start/stop LRC
    start_lrc_kwargs = dict()
    start_lrc_kwargs.update(**config.server_config)
    start_lrc_kwargs.update(**config.waiter_config)
    if 'start_lrc' in commands_kwargs:
        start_lrc_kwargs.update(**commands_kwargs['start_lrc'])
    if register_remotely:
        remote_command_config['start_lrc'] = {
            "import":"LRC.Server.Commands.LRCServer",
            "execute":"start_lrc",
            "kwargs": start_lrc_kwargs
        }
        remote_command_config['stop_lrc'] = {
            "import":"LRC.Server.Commands.LRCServer",
            "execute":"stop_lrc"
        }
    else:
        command_server.register_command('start_lrc', Command(name='start_lrc', execute=start_lrc, kwargs=start_lrc_kwargs))
        command_server.register_command('stop_lrc', Command(name='stop_lrc', execute=stop_lrc))

    # start/stop LRC server
    start_lrc_server_kwargs = dict()
    start_lrc_server_kwargs.update(**config.server_config)
    if 'start_lrc_server' in commands_kwargs:
        start_lrc_server_kwargs.update(**commands_kwargs['start_lrc_server'])
    if register_remotely:
        remote_command_config['start_lrc_server'] = {
            "import":"LRC.Server.Commands.LRCServer",
            "execute":"start_lrc_server",
            "kwargs": start_lrc_server_kwargs
        }
        remote_command_config['stop_lrc_server'] = {
            "import":"LRC.Server.Commands.LRCServer",
            "execute":"stop_lrc_server"
        }
    else:
        command_server.register_command('start_lrc_server', Command(name='start_lrc_server', execute=start_lrc_server, kwargs=start_lrc_server_kwargs))
        command_server.register_command('stop_lrc_server', Command(name='stop_lrc_server', execute=stop_lrc_server))

    # start/stop LRC waiter
    start_lrc_waiter_kwargs = dict()
    start_lrc_waiter_kwargs.update(**config.waiter_config)
    if 'start_lrc_waiter' in commands_kwargs:
        start_lrc_waiter_kwargs.update(**commands_kwargs['start_lrc_waiter'])
    if register_remotely:
        remote_command_config['start_lrc_waiter'] = {
            "import":"LRC.Server.Commands.LRCServer",
            "execute":"start_lrc_waiter",
            "kwargs": start_lrc_waiter_kwargs
        }
        remote_command_config['stop_lrc_waiter'] = {
            "import":"LRC.Server.Commands.LRCServer",
            "execute":"stop_lrc_waiter"
        }
    else:
        command_server.register_command('start_lrc_waiter', Command(name='start_lrc_waiter', execute=start_lrc_waiter, kwargs=start_lrc_waiter_kwargs))
        command_server.register_command('stop_lrc_waiter', Command(name='stop_lrc_waiter', execute=stop_lrc_waiter))

    # quit LRC
    if register_remotely:
        remote_command_config['quit_lrc'] = {
            "import":"LRC.Server.Commands.LRCServer",
            "execute":"quit",
        }
        command_server.send_command('register_cleanup_command', args=('quit_lrc',))
    else:
        command_server.register_command('quit_lrc', Command(name='quit_lrc', execute=quit_lrc))
        command_server.register_cleanup_command('quit_lrc')

    # execute register command remotely
    if register_remotely:
        command_server.register_command_remotely(remote_command_config)


def _help_commands():
    return '''
LRC server
[Usage]
    lrcserver [options] command1 command1-params command2 command2-params ...

[options]
    --help, -h              show this help info
    --version               show LRC version
    --no-ui                 disable server UI, UI is disable by default
    --enable-ui             enable server UI
    --verbose               show more information in log
    --config-file=FILEPATH  load LRC configurations from FILEPATH(json file format)

[commands]
    start_lrc               start LRC server and waiter
        server_address      LRC server address
        waiter_address      LRC waiter address
        verify_code         LRC connection verify code
        verbose             verbose info switch
    start_lrc_server        start LRC server
        server_address      LRC server address
        waiter_address      LRC waiter address
        verify_code         LRC connection verify code
        verbose             verbose info switch
    start_lrc_waiter        start LRC waiter
        server_address      LRC server address
        waiter_address      LRC waiter address
        verbose             verbose info switch
    stop_lrc                stop LRC server and waiter
    stop_lrc_server         stop LRC server
    stop_lrc_waiter         stop LRC waiter
    quit                    quit all process


[example]
    lrcserver --no-ui start_lrc server_address=('0.0.0.0',35589)
    lrcserver stop_lrc      # you may need to run this in another command window

[more]
    for more infomation, see https://github.com/davied9/LANRemoteController
    '''

if __name__ == '__main__':
    main()
