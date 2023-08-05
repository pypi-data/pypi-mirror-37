# -*-coding:utf-8-*-
from __future__ import print_function
import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from multiprocessing import Process, Manager, freeze_support
from threading import Thread
from random import randint
from time import sleep
from LRC.Common.logger import logger
from LRC.Common.empty import empty
from LRC.Server.LRCServer import LRCServer, LRCWaiter
import re, os
os.environ['KIVY_IMAGE'] = 'pil,sdl2'



def start_LRCServer(server_address, waiter_address, verify_code, client_list, log_mailbox=None, verbose=False):
    LRCServer(server_address=server_address,
              waiter_address=waiter_address,
              verify_code=verify_code,
              client_list=client_list,
              log_mailbox=log_mailbox,
              verbose=verbose).serve_forever()


def start_LRCWaiter(waiter_address, server_address, client_list, log_mailbox=None, verbose=False):
    LRCWaiter(waiter_address=waiter_address,
              server_address=server_address,
              client_list=client_list,
              log_mailbox=log_mailbox,
              verbose=verbose).serve_forever()


class _log_buffer(object):

    def __init__(self, max_size=10, pop_size=1):
        self.buffer = []
        self.max_size = max_size
        self.pop_size = pop_size

    def clear(self):
        self.buffer = []

    def log(self, info):
        if len(self.buffer) >= self.max_size:
            self.buffer = self.buffer[self.pop_size:]
        self.buffer.append(str(info))

    def pack_messages(self):
        str = ''
        for info in self.buffer:
            str += ( info + '\n')
        return str

    @property
    def size(self):
        return len(self.buffer)



class LRCServerUI(App):

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, val):
        self._verbose = val
        if val: self.verbose_info = self._verbose_info_imp
        else:   self.verbose_info = empty

    # interfaces
    def __init__(self, *, verbose=False,
                 server_address=('0.0.0.0', 35530), waiter_address=('0.0.0.0', 35527),
                 watch_interval=0.5, **kwargs):
        super(LRCServerUI, self).__init__(**kwargs)
        # servers
        self.server_address = server_address
        self.server_process = None
        self.waiter_address = waiter_address
        self.waiter_process = None
        self.watch_interval = watch_interval
        # regexp
        self.ip_matcher = re.compile(r'(\d+)\.(\d+)\.(\d+)\.(\d+)')
        self.comm_manager = Manager()
        # client list
        self.client_list = self.comm_manager.list()
        # log buffer
        self.log_mailbox = self.comm_manager.Queue()
        self.log_buffer = _log_buffer(max_size=100, pop_size=1)
        # state
        self.running = False
        # other configurations
        self.verbose = verbose

    def build(self):
        # UI
        self.root = BoxLayout(orientation='vertical')
        #   up : start/stop buttons
        width_button = 0.15
        width_IP_label = 40
        width_IP_input = 0.15
        width_port_label = 60
        width_port_input = 0.15
        width_info_label = 1 - width_button - width_IP_input - width_port_input - 0.1
        up_grid = GridLayout(cols=6, padding=10, spacing=10, size_hint=(1, None), height=100)
        self.root.add_widget(up_grid)
        self.server_button      = Button(text="Start Server", size_hint_x=width_button, on_release=self.on_start_server_pressed)
        self.server_info_label  = Label(halign='left', valign='center', size_hint_x=width_info_label)
        self.server_info_label.bind(size=self._sync_size_to_text_size)
        self.server_ip_input    = TextInput(text=self.server_address[0], size_hint_x=width_IP_input)
        self.server_port_input  = TextInput(text=str(self.server_address[1]), size_hint_x=width_port_input)
        self.waiter_button      = Button(text="Start Waiter", size_hint_x=width_button, on_release=self.on_start_waiter_pressed)
        self.waiter_info_label  = Label(halign='left', valign='center', size_hint_x=width_info_label)
        self.waiter_info_label.bind(size=self._sync_size_to_text_size)
        self.waiter_ip_input    = TextInput(text=self.waiter_address[0], size_hint_x=width_IP_input)
        self.waiter_port_input  = TextInput(text=str(self.waiter_address[1]), size_hint_x=width_port_input)
        up_grid.add_widget(self.server_button)
        up_grid.add_widget(Label(text="IP", size_hint_x=None, width=width_IP_label))
        up_grid.add_widget(self.server_ip_input)
        up_grid.add_widget(Label(text="Port", size_hint_x=None, width=width_port_label))
        up_grid.add_widget(self.server_port_input)
        up_grid.add_widget(self.server_info_label)
        up_grid.add_widget(self.waiter_button)
        up_grid.add_widget(Label(text="IP", size_hint_x=None, width=width_IP_label))
        up_grid.add_widget(self.waiter_ip_input)
        up_grid.add_widget(Label(text="Port", size_hint_x=None, width=width_port_label))
        up_grid.add_widget(self.waiter_port_input)
        up_grid.add_widget(self.waiter_info_label)
        #   down : log window
        self.log_window = Label(size_hint_y=None)
        self.log_window.bind(size=self._sync_size_to_text_size)
        scroll_view = ScrollView()
        scroll_view.add_widget(self.log_window)
        self.root.add_widget(scroll_view)
        return self.root

    def update_config(self, *,
            server_address=None,
            waiter_address=None,
            verbose=False,
            **kwargs # for all the junks
        ):
        self.verbose = verbose
        if verbose:
            self._verbose_info = self.log
        if server_address:
            self.server_address = server_address
            self.server_ip_input.text = str(server_address[0])
            self.server_port_input.text = str(server_address[1])
        if waiter_address:
            self.waiter_address = waiter_address
            self.waiter_ip_input.text = str(waiter_address[0])
            self.waiter_port_input.text = str(waiter_address[1])

    def on_start(self):
        self.running = True
        Thread(target=self._mailbox_watcher).start()

    def on_stop(self):
        self.running = False
        self.comm_manager.shutdown()
        self.stop_waiter()
        self.stop_server()

    def log(self, message):
        logger.info(message)
        self.log_buffer.log(message)
        self.log_window.height = (self.log_buffer.size + 1) * (self.log_window.font_size * 1.25)
        self.log_window.text = self.log_buffer.pack_messages()

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

    def start_server(self):
        try:
            # parse waiter address
            ip = self.parse_ip(self.waiter_ip_input.text)
            port = self.parse_port(self.waiter_port_input.text)
            waiter_address = (ip, port)
            # parse server address
            ip = self.parse_ip(self.server_ip_input.text)
            port = self.parse_port(self.server_port_input.text)
            server_address = (ip, port)
        except ValueError as err:
            waiter_address = None
            server_address = None
            self.log('Server: start server failed, unable to parse ip or port : {0}'.format(err.args))
        if server_address:
            self.server_address = server_address
            self.waiter_address = waiter_address
            self.log('Server: start server at : {0}, bind to waiter {1}'.format(self.server_address, self.waiter_address))
            self.server_button.text = 'Close Server'
            self.server_code = str(randint(1000, 9999))
            self.server_info_label.text = 'code : ' + self.server_code + ', running ...'
            self.server_ip_input.disabled = True
            self.server_port_input.disabled = True
            self.server_process = Process(target=start_LRCServer, args=(self.server_address, self.waiter_address, self.server_code, self.client_list, self.log_mailbox, self.verbose))
            self.server_process.start()
            Thread(target=self._server_watcher).start()

    def stop_server(self):
        if self.server_process:
            self.log('Server: terminate server ')
            self.server_process.terminate()
            self.server_process = None
            self.server_button.text = 'Start Server'
            self.server_code = None
            self.server_info_label.text = ''
            self.server_ip_input.disabled = False
            self.server_port_input.disabled = False

    def start_waiter(self):
        if not self.server_process:
            self.log('Server: server should be started first')
            return
        try:
            ip = self.parse_ip(self.waiter_ip_input.text)
            port = self.parse_port(self.waiter_port_input.text)
            waiter_address = (ip, port)
        except ValueError as err:
            waiter_address = None
            self.log('Server: start waiter failed, unable to parse ip or port : {0}'.format(err.args))
        if waiter_address:
            self.waiter_address = waiter_address
            self.log('Server: start waiter at : {0}'.format( self.waiter_address ))
            self.waiter_button.text = 'Close Waiter'
            self.waiter_info_label.text = 'running ...'
            self.waiter_ip_input.disabled = True
            self.waiter_port_input.disabled = True
            self.waiter_process = Process(target=start_LRCWaiter, args=(self.waiter_address, self.server_address, self.client_list, self.log_mailbox, self.verbose))
            self.waiter_process.start()
            Thread(target=self._waiter_watcher).start()

    def stop_waiter(self):
        if self.waiter_process:
            self.log('Server: terminate waiter ')
            self.waiter_process.terminate()
            self.waiter_process = None
            self.waiter_button.text = 'Start Waiter'
            self.waiter_info_label.text = ''
            self.waiter_ip_input.disabled = False
            self.waiter_port_input.disabled = False

    # functional
    def _sync_size_to_text_size(self, component, new_size):
        component.text_size = new_size

    def _server_watcher(self):
        while True:
            if not self.server_process:
                break
            if not self.server_process.is_alive():
                self.stop_server()
                break
            sleep(self.watch_interval)

    def _waiter_watcher(self):
        while True:
            if not self.waiter_process:
                break
            if not self.waiter_process.is_alive():
                self.stop_waiter()
                break
            sleep(self.watch_interval)

    def _mailbox_watcher(self):
        while True:
            try:
                self.log(self.log_mailbox.get()) # get will block until there is data
            except Exception as err:
                if not self.running:
                    self.log('Server : closing servers.')
                    break
                else:
                    self.log('Error : {}'.format(err))

    def on_start_server_pressed(self, inst):
        if self.server_process: # process is running, close it
            self.stop_server()
        else: # start new server
            self.start_server()

    def on_start_waiter_pressed(self, inst):
        if self.waiter_process: # process is running, close it
            self.stop_waiter()
        else: # start new waiter
            self.start_waiter()

    def _verbose_info_imp(self, info):
        self.log('Server : [verbose] {}'.format(info))


if __name__ == '__main__':
    freeze_support()
    logger.set_logger(name='kivy')
    LRCServerUI().run()
    pass

