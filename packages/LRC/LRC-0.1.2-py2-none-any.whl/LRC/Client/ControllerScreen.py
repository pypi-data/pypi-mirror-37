import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.properties import NumericProperty
from LRC.Client.ButtonContainer import ButtonContainer

Builder.load_string('''
#:import LRCClientConnector LRC.Client.LRCClientConnector
#:import ButtonContainer    LRC.Client.ButtonContainer

<ControllerScreen>:
    # widgets
    background_layout: background_layout
    display_title: title_label
    connector: connector
    info_label: info_label
    button_container: button_container
    # layout
    BoxLayout:
        id: background_layout
        orientation: 'vertical'
        padding: 30, 0
        Widget:
            size_hint: 1, 0.05
        BoxLayout:
            size_hint: 1, 0.1
            Button:
                text: 'Back'
                size_hint_x: 0.2
                on_release: root._go_back_last_screen(self)
            Label:
                id: title_label
                text: 'Default'
                font_size: 43
            Button:
                text: 'Edit'
                size_hint_x: 0.2
                on_release: root._goto_builder_screen(self)
        Widget:
            size_hint: 1, 0.05
        ButtonContainer:
            id: button_container
        Widget:
            size_hint: 1, 0.05
        LRCClientConnector:
            id: connector
            size_hint: 1, 0.1
        Label:
            id: info_label
            size_hint: 1, 0.05
            font_size: 25
            color: 1, 0, 0, 1
''')


class ControllerScreen(Screen): # controller operation room

    button_height = NumericProperty(0)
    button_spacing = NumericProperty(0)

    def __init__(self, **kwargs):
        super(ControllerScreen, self).__init__(**kwargs)
        self.ip_and_port_input = None
        Clock.schedule_once(self._delayed_init)

    def _delayed_init(self, *args):
        # do some bindings
        self.connector.ip_button.bind(on_release=self._on_ip_button_released)
        self.connector.port_button.bind(on_release=self._on_port_button_released)
        # initialize
        self.connector.ext_err_logger = self.present_info


    def on_pre_enter(self, *args):
        current_app = App.get_running_app()

        self._reset_button_container()
        for _, controller in current_app.controller_sets[current_app.current_edit_set].controllers.items():
            self._add_controller_button(controller)

        self.display_title.text = current_app.current_edit_set

        if current_app.client.server_address:
            self.connector.ip_button.text   = current_app.client.server_address[0]
            self.connector.port_button.text = str(current_app.client.server_address[1])


    def _reset_button_container(self):
        self.button_container.clear_buttons()

    def _add_controller_button(self, controller):
        button = Button( text=controller.name, on_release=self._on_controller_button_released )
        button.controller = controller
        self.button_container.add_button(button)

    def _go_back_last_screen(self, button):
        App.get_running_app().current_edit_set = self.display_title.text

        last_screen = self.manager.last_screen
        self.manager.last_screen = "Controller Collections"
        self.manager.current = last_screen

    def _goto_builder_screen(self, button): # Edit current controller collection
        App.get_running_app().current_edit_set = self.display_title.text
        self.manager.last_screen = "Controller"
        self.manager.current = 'Controller Collection Builder'

    def _on_controller_button_released(self, button):
        try:
            self._execute_controller(button.controller)
        except:
            self.present_info('Controller: failed to execute controller, maybe server is not connected???')

    def _execute_controller(self, controller):
        self.connector.execute_controller(controller)

    # ip_or_port = 'ip' or 'port'
    def _open_ip_port_input(self, button, ip_or_port):
        if not self.ip_and_port_input:
            self.ip_and_port_input = TextInput(text=button.text, size_hint_y=0.1)
            self.ip_and_port_input.bind(focused=self._on_ip_or_port_input_focused)
            self.background_layout.add_widget(self.ip_and_port_input, 999)

        if 'ip' == ip_or_port:
            self.ip_and_port_input.sync_button = self.connector.ip_button
        else:
            self.ip_and_port_input.sync_button = self.connector.port_button

        self.ip_and_port_input.text = self.ip_and_port_input.sync_button.text

    # as callback for ip_button
    def _on_ip_button_released(self, button):
        self._open_ip_port_input(button, 'ip')

    # as callback for port_button
    def _on_port_button_released(self, button):
        self._open_ip_port_input(button, 'port')

    # as callback for ip or port input
    def _on_ip_or_port_input_focused(self, input, focused):
        if focused:
            input.select_all()
        else:
            input.sync_button.text = input.text
            self.background_layout.remove_widget(input)
            self.ip_and_port_input = None

    def present_info(self, info, time_last=5):
        self.info_label.text = info
        self.clear_info_event = Clock.schedule_once(self._clear_info_helper, time_last)

    def _clear_info_helper(self, *args): # the argument passed maybe the position of touch
        self.info_label.text = ''
        self.clear_info_event = None
