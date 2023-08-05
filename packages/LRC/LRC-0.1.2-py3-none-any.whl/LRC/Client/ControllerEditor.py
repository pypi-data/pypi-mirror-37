import kivy
kivy.require('1.10.1')

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
<ControllerEditor>:
    size_hint: 1, None
    height: 100
    left_ctrl_checkbox:     left_ctrl_checkbox
    right_ctrl_checkbox:    right_ctrl_checkbox
    left_shift_checkbox:    left_shift_checkbox
    right_shift_checkbox:   right_shift_checkbox
    left_alt_checkbox:      left_alt_checkbox
    right_alt_checkbox:     right_alt_checkbox
    controller_name_editor: controller_name_editor
    controller_key_editor:  controller_key_editor
    GridLayout:
        size_hint: 0.45, 1
        cols: 3
        rows: 4
        Widget:
        Label:
            text: 'left'
        Label:
            text: 'right'
        Label:
            text: 'ctrl'
        CheckBox:
            id: left_ctrl_checkbox
            group: 'group_control'
        CheckBox:
            id: right_ctrl_checkbox
            group: 'group_control'
        Label:
            id: shift_label
            text: 'shift'
        CheckBox:
            id: left_shift_checkbox
            group: 'group_shift'
        CheckBox:
            id: right_shift_checkbox
            group: 'group_shift'
        Label:
            id: alt_label
            text: 'alt'
        CheckBox:
            id: left_alt_checkbox
            group: 'group_alternative'
        CheckBox:
            id: right_alt_checkbox
            group: 'group_alternative'
    BoxLayout:
        size_hint: 0.2, 1
        orientation: 'vertical'
        Label:
            text: 'name'
        Label:
            text: 'key'
    BoxLayout:
        size_hint: 0.35, 1
        orientation: 'vertical'
        Widget:
            size_hint: 1,0.05
        TextInput:
            size_hint: 1,0.4
            id: controller_name_editor
            multiline: False
        Widget:
            size_hint: 1,0.1
        TextInput:
            size_hint: 1,0.4
            id: controller_key_editor
            multiline: False
        Widget:
            size_hint: 1,0.05
''')


class ControllerEditor(BoxLayout):
    '''Controller Editor

    components:
        controller:     Controller that is being edit
    '''

    def __init__(self, **kwargs):
        self.controller = kwargs["controller"]
        self.controller_button = kwargs["controller_button"]
        del(kwargs['controller'], kwargs['controller_button'])
        super(ControllerEditor, self).__init__(**kwargs)
