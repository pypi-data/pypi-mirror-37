import kivy
kivy.require('1.10.1')

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from LRC.Common.logger import logger
import re

Builder.load_string('''
<LRCClientConnector>:
    ip_label: ip_label
    ip_button: ip_button
    port_label: port_label
    port_button: port_button
    Button:
        text: 'Connect'
        size_hint: 0.2, 1
        on_release: root.on_connect_released(self)
    Label:
        id: ip_label
        text: 'IP'
        size_hint: 0.1, 1
    Button:
        id: ip_button
        text: '127.0.0.1'
        size_hint: 0.3, 1
        background_color: [0, 0, 0, 0]
    Label:
        id: port_label
        text: 'Port'
        size_hint: 0.1, 1
    Button:
        id: port_button
        text: '35530'
        size_hint: 0.3, 1
        background_color: [0, 0, 0, 0]
''')


class LRCClientConnector(BoxLayout):

    def __init__(self, **kwargs):
        self.client = App.get_running_app().client
        super(LRCClientConnector, self).__init__(**kwargs)
        self.ip_matcher = re.compile(r'(\d+)\.(\d+)\.(\d+)\.(\d+)')
        self.ext_err_logger = None

    def execute_controller(self, controller):
        for _, comb in controller.dump().items():
            combination = comb
        self.client.send_combinations(*combination)

    # as callback for "Connect" button
    def on_connect_released(self, button):
        try:
            ip = self.parse_ip(self.ip_button.text)
            port = self.parse_port(self.port_button.text)
            server_address = (ip, port)
        except ValueError as err:
            server_address = None
            info = 'Connector: start server failed, unable to parse ip or port : {0}'.format(err.args)
            logger.info(info)
            if self.ext_err_logger: self.ext_err_logger(info)
        if server_address:
            try:
                self.connect(server_address)
            except Exception as err:
                info = 'Connector: try to connect to {0} failed: {1}'.format(server_address, err.args)
                logger.info(info)
                if self.ext_err_logger: self.ext_err_logger(info)

    def connect(self, server_address):
        self.client.connect(server_address)

    def parse_ip(self, str):
        if '' == str or 'localhost' == str:
            str = '127.0.0.1'
        else:
            vols, = self.ip_matcher.findall(str)
            if len(vols) != 4:
                raise ValueError('ip not correct, must be "xxx.xxx.xxx.xxx", "xxx" should between [0,255]')
            ip_list = []
            for vol in vols:
                val = int(vol)
                if val < 0 or val > 255:
                    raise ValueError('ip should be between [0,255], found %d' % val)
                ip_list.append(vol)
                ip_list.append('.')
            str = ''.join(ip_list[:-1])
        return str

    def parse_port(self, str):
        port = int(str)
        if port > 10000 and port < 49999:
            return port
        else:
            raise ValueError('port should between (10000, 49999)')
