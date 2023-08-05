import json

class LRCServerConfig(object):

    # basics
    def __init__(self, **kwargs):
        # initialize default values
        self._init_default_values()
        # load config files
        if 'config_file' in kwargs:
            self.config_file = kwargs['config_file']
        # apply configurations from arguments
        self._update_command_server_config(**kwargs)
        self._update_server_config(**kwargs)
        self._update_waiter_config(**kwargs)
        if 'enable_ui' in kwargs:
            self.enable_ui = kwargs['enable_ui']
        if 'verify_code' in kwargs: # for new client verification
            self.verify_code = kwargs['verify_code']
        if 'verbose' in kwargs:
            self.verbose = kwargs['verbose']

    def __str__(self):
        return '''
    config file             : {},
    command server address  : {},
    server address          : {},
    waiter address          : {},
    UI enabled              : {},
    verify code             : {},
    verbose                 : {},
'''.format(
            self.config_file,
            self.command_server_address,
            self.server_address,
            self.waiter_address,
            self.enable_ui,
            self.verify_code,
            self.verbose,
        )

    # properties
    @property
    def config_file(self):
        return self._config_file

    @config_file.setter
    def config_file(self, config_file):
        if config_file:
            self.load_from_config_file(config_file)
        else:
            self._config_file = None

    @property
    def command_server_address(self):
        return (self.command_ip, self.command_port)

    @property
    def server_address(self):
        return (self.server_ip, self.server_port)

    @property
    def waiter_address(self):
        return (self.waiter_ip, self.waiter_port)

    @property
    def command_server_config(self):
        return {
            'server_address' : self.command_server_address,
            'verbose'         : self.verbose,
        }

    @property
    def server_config(self):
        return {
            'server_address' : self.server_address,
            'waiter_address' : self.waiter_address,
            'verify_code'    : self.verify_code,
            'verbose'         : self.verbose,
        }

    @property
    def waiter_config(self):
        return {
            'server_address'  : self.server_address,
            'waiter_address'  : self.waiter_address,
            'verbose'         : self.verbose,
        }


    # interfaces
    def apply_config(self, **kwargs): # apply all config except config_file, this is maintained by load_from_config_file
        self._update_command_server_config(**kwargs)
        self._update_waiter_config(**kwargs)
        self._update_server_config(**kwargs)
        if 'enable_ui' in kwargs:
            self.enable_ui = kwargs['enable_ui']
        if 'verify_code' in kwargs:
            self.verify_code = kwargs['verify_code']
        if 'verbose' in kwargs:
            self.verbose = kwargs['verbose']

    def dump_to_dict(self):
        d = dict()
        d['command_server_address'] = self.command_server_address
        d['server_address'] = self.server_address
        d['waiter_address'] = self.waiter_address
        d['enable_ui'] = self.enable_ui
        d['verify_code'] = self.verify_code
        d['verbose'] = self.verbose
        return d

    def load_from_config_file(self, config_file):
        with open(config_file, 'r') as fp:
            config_string = fp.read()
        config_dict = json.loads(config_string)
        self.apply_config(**config_dict)
        self._config_file = config_file

    def save_to_config_file(self, config_file):
        d = self.dump_to_dict()
        str = json.dumps(d)
        with open(config_file, 'w') as fp:
            fp.write(str)

    # functional
    def _init_default_values(self):
        self._config_file = None
        self.enable_ui = False

        self.command_ip = '127.0.0.1'
        self.command_port = 32781

        self.server_ip = '0.0.0.0'
        self.server_port = 35530

        self.waiter_ip = '0.0.0.0'
        self.waiter_port = 35527

        self.verify_code = None # for new client verification
        self.verbose = False

    # details
    def _update_command_server_config(self, **kwargs):
        if 'command_server_address' in kwargs:
            self.command_ip = kwargs['command_server_address'][0]
            self.command_port = kwargs['command_server_address'][1]
        if 'command_server_ip' in kwargs:
            self.command_ip = kwargs['command_server_ip']
        if 'command_server_port' in kwargs:
            self.command_port = kwargs['command_server_port']

    def _update_server_config(self, **kwargs):
        if 'server_address' in kwargs:
            self.server_ip = kwargs['server_address'][0]
            self.server_port = kwargs['server_address'][1]
        if 'server_ip' in kwargs:
            self.server_ip = kwargs['server_ip']
        if 'server_port' in kwargs:
            self.server_port = kwargs['server_port']

    def _update_waiter_config(self, **kwargs):
        if 'waiter_address' in kwargs:
            self.waiter_ip = kwargs['waiter_address'][0]
            self.waiter_port = kwargs['waiter_address'][1]
        if 'waiter_ip' in kwargs:
            self.waiter_ip = kwargs['waiter_ip']
        if 'waiter_port' in kwargs:
            self.waiter_port = kwargs['waiter_port']


if '__main__' == __name__:
    import os
    config = LRCServerConfig()
    print('config : {}'.format(config))
    print('config dump dict : {}'.format(config.dump_to_dict()))

    save_config_file = os.path.join('LRC', 'test_config.ini')
    save_config_file = os.path.abspath(save_config_file)
    print('save config to file : {}'.format(save_config_file))
    config.save_to_config_file(save_config_file)
    # following is saved content :
    # {
    #     "verbose": false,
    #     "server_address": ["0.0.0.0", 35530],
    #     "enable_ui": false,
    #     "command_server_address": ["127.0.0.1", 32781],
    #     "waiter_address": ["0.0.0.0", 35527],
    #     "verify_code": null
    # }

    load_config_file = os.path.join('LRC', 'config.json')
    load_config_file = os.path.abspath(load_config_file)
    config.load_from_config_file(load_config_file)
    print('config loaded from config file {} : {}'.format(load_config_file, config))
    # following is loaded content :
    # config_file             : <working directory>\LRC\config.json,
    # command server address  : ('0.0.0.0', 35589),
    # server address          : ('0.0.0.0', 35530),
    # waiter address          : ('0.0.0.0', 33171),
    # UI enabled              : False,
    # verify code             : None,
    # verbose                 : True,
