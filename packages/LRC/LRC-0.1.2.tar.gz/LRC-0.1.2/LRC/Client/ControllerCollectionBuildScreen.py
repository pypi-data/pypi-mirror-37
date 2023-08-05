import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from LRC.Common.logger import logger
from LRC.Common.Exceptions import NotFoundError
from LRC.Controller.LRCController import Controller, ControllerSet
from LRC.Client.ControllerEditor import ControllerEditor
from LRC.Client.ButtonContainer import ButtonContainer

Builder.load_string('''
#:import ButtonContainer    LRC.Client.ButtonContainer

<ControllerCollectionBuildScreen>:
    display_title: title_button
    background_floatlayout: background_floatlayout
    background_layout: background_layout
    delete_button: delete_button
    info_label: info_label
    button_container: button_container
    FloatLayout:
        id: background_floatlayout
        BoxLayout:
            id: background_layout
            orientation: 'vertical'
            padding: 30, 30
            Button:
                id: title_button
                text: 'Builder'
                size_hint: 1, 0.2
                font_size: 43
                background_color: [0, 0, 0, 0]
                on_release: root._open_set_name_editor(self, self.text)
            ButtonContainer:
                id: button_container
            BoxLayout:
                size_hint: 1, 0.2
                padding: 10, 30, 10, 0 # left, top, right, down
                Button:
                    text: 'Back'
                    size_hint: 0.2, 1
                    on_release: root._go_back_last_screen(self)
                Widget:
                    size_hint: 0.05, 1
                ToggleButton:
                    id: delete_button
                    text: 'Delete'
                    size_hint: 0.2, 1
                    on_release: root._on_delete_button_released(self, self.state)
                Widget:
                    size_hint: 0.05, 1
                Button:
                    text: 'Save'
                    size_hint: 0.2, 1
                    on_release: root._save_controller_set(self)
                Widget:
                    size_hint: 0.05, 1
                Button:
                    text: 'Add'
                    size_hint: 0.2, 1
                    on_release: root._create_new_button(self)
        Label:
            id: info_label
            font_size: 12
            color: 1, 0, 0, 1
            pos_hint: {'x':0, 'y':0}
            size_hint: 1, 0.05

''')


class ControllerCollectionBuildScreen(Screen): # controller collection builder
    '''Controller Collection Build Screen
    use "set" instead of "Collection" in code for short

    components:
        display_title:              title Button
        button_container:           button container for controllers
        background_floatlayout:     background FloatLayout
        info_label:                 information label with read font, meant for error message

        set_name_editor:            controller collection TextInput
        controller_editor:          controller editor
        clear_info_event:           an event to clear info label

        controller_button_process:  function handle of process -- delete or edit,
                                    decide interactive feature of controller button

    '''

    set_name_editor = ObjectProperty(None, allownone=True)
    controller_editor = ObjectProperty(None, allownone=True)
    clear_info_event = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        self.controller_button_process = self._process_edit_interact
        super(ControllerCollectionBuildScreen, self).__init__(**kwargs)

    def on_pre_enter(self, *args):
        current_app = App.get_running_app()
        if current_app.current_edit_set:
            # set display name
            self.display_title.text = current_app.current_edit_set
            # add controller buttons
            for _, controller in current_app.controller_sets[current_app.current_edit_set].controllers.items():
                self._add_controller_button(controller)
        else:
            self.display_title.text = self._get_next_new_controller_set_name()
            current_app.current_edit_set = self.display_title.text
            current_app.controller_sets[self.display_title.text] = ControllerSet(self.display_title.text)

    def on_leave(self, *args):
        self._reset_controller_set_container()
        self._clear_info_helper()

    def present_info(self, info, time_last=5):
        self.info_label.text = info
        self.clear_info_event = Clock.schedule_once(self._clear_info_helper, time_last)

    def _clear_info_helper(self, *args): # the argument passed maybe the position of touch
        self.info_label.text = ''
        self.clear_info_event = None

    # as callback for display_title on_release
    def _open_set_name_editor(self, *args):
        logger.info('Builder: open set name editor {0}'.format(self.display_title.text))
        # disable display_title to avoid re-call of _open_set_name_editor
        self.display_title.disabled = True
        # create set_name_editor
        if self.set_name_editor is None:
            self.set_name_editor = TextInput(
                size_hint=[ None, None],
                font_size=43,
                multiline=False
            )
            self.background_floatlayout.add_widget(self.set_name_editor)
        self.set_name_editor.size = self.display_title.size
        self.set_name_editor.pos  = self.display_title.pos
        self.set_name_editor.text = self.display_title.text
        self.set_name_editor.bind(focused=self._on_focused_set_name_editor)
        # bind size && pos, call sync once manually to sync pos && size
        self.display_title.bind(size=self._sync_display_title_size_to_set_name_editor)
        self.display_title.bind(pos=self._sync_display_title_pos_to_set_name_editor)

    # as callback for set_name_editor focus
    def _on_focused_set_name_editor(self, _set_name_eidtor, focused):
        if focused:
            _set_name_eidtor.select_all()
        else:
            current_app = App.get_running_app()
            current_edit_set = current_app.controller_sets[current_app.current_edit_set]
            if not self._exist_duplicate_controller_set(self.set_name_editor.text, current_edit_set):
                new_set_name = self.set_name_editor.text
                if new_set_name:
                    self.display_title.text = new_set_name
                    self._rename_current_edit_set(new_set_name)
                    self._close_set_name_editor()
                else:
                    self.present_info('Duplicate controller collection {0}'.format(self.set_name_editor.text))
            else:
                self.present_info('Duplicate controller collection {0}'.format(self.set_name_editor.text))

    def _close_set_name_editor(self, *args):
        logger.info('Builder: close set name editor {0}'.format(self.display_title.text))
        self.display_title.unbind(size=self._sync_display_title_size_to_set_name_editor)
        self.display_title.unbind(pos=self._sync_display_title_pos_to_set_name_editor)
        self.display_title.disabled = False
        self.background_floatlayout.remove_widget(self.set_name_editor)
        self.set_name_editor = None

    def _rename_current_edit_set(self, new_set_name):
        current_app = App.get_running_app()
        # get controller set and remove it from dict
        _set = current_app.controller_sets[current_app.current_edit_set]
        del(current_app.controller_sets[current_app.current_edit_set])
        # rename && add to dict with new name
        _set.name = new_set_name
        current_app.controller_sets[new_set_name] = _set
        # sync to tag
        current_app.current_edit_set = new_set_name

    # as callback for display_title pos
    def _sync_display_title_pos_to_set_name_editor(self, _display_title, new_pos):
        self.set_name_editor.pos = new_pos

    # as callback for display_title size
    def _sync_display_title_size_to_set_name_editor(self, _display_title, new_size):
        self.set_name_editor.size = new_size

    # add controller button to controller container for controller
    def _add_controller_button(self, controller):
        for name, value in controller.dump().items():
            text = name + '  :  ' + str(value)
        button = Button( text=text, on_release=self._on_controller_button_released )
        button.controller = controller
        self.button_container.add_button(button)

    # remove controller button from controller container
    def _remove_controller_button(self, controller_button):
        self.button_container.remove_button(controller_button)

    # as callback for "Save" button -- save this build to a controller set file
    def _save_controller_set(self, button):
        current_app = App.get_running_app()
        controller_set = current_app.controller_sets[current_app.current_edit_set]
        controller_set.dump_to_file('./collections/{0}.json'.format(current_app.current_edit_set))

        self._revert_delete_button_state()

    # as callback for "Add" button -- add button for new created controller
    def _create_new_button(self, button):
        new_controller = Controller(self._get_next_new_controller_name(), 'n')
        self._add_controller_button(new_controller)
        self._add_controller_to_editing_set(new_controller)

        self._revert_delete_button_state()

    # as callback for "Back" button
    def _go_back_last_screen(self, button):
        if self.set_name_editor:
            self._close_set_name_editor()

        if self.controller_editor:
            self._close_controller_editor()

        last_screen = self.manager.last_screen
        self.manager.last_screen = "Controller Collections"
        self.manager.current = last_screen

        self._revert_delete_button_state()

    # as callback for controller button
    def _on_controller_button_released(self, controller_button):
        self.controller_button_process(controller_button)

    # as callback for "Delete" button
    def _on_delete_button_released(self, button, state):
        if 'down' == state:
            self.controller_button_process = self._process_delete_interact
        else:
            self.controller_button_process = self._process_edit_interact

    def _revert_delete_button_state(self):
        if 'down' == self.delete_button.state:
            self.delete_button.state = 'normal'

    def _process_edit_interact(self, controller_button):
        # not editing
        if not self.controller_editor:
            self._open_controller_editor(controller_button)
        # editing, sync and close
        else:
            try:
                # editing this
                if self.controller_editor.controller is controller_button.controller:
                    self._sync_controller_editor_to_controller()
                    self._close_controller_editor()
                # editing another
                else:
                    self._sync_controller_editor_to_controller()
                    self._close_controller_editor()
                    self._open_controller_editor(controller_button)
            except Controller.UnsupportedKeyForControllerError as err: # unsupported key
                self.present_info(str(err))
            except ControllerCollectionBuildScreen.DuplicateError as err: # duplicated Controller
                self.present_info(str(err))

    def _process_delete_interact(self, controller_button):
        # not editing or editing others, just delete
        if self.controller_editor and self.controller_editor.controller is controller_button.controller:
            self._close_controller_editor()
        self._remove_controller_from_editing_set(controller_button.controller)
        self._remove_controller_button(controller_button)

    # add controller to current editing controller collection
    def _add_controller_to_editing_set(self, controller):
        current_app = App.get_running_app()
        _set = current_app.controller_sets[current_app.current_edit_set]
        _set.add_controller(controller)

    # remove controller from current editing controller collection
    def _remove_controller_from_editing_set(self, controller):
        current_app = App.get_running_app()
        _set = current_app.controller_sets[current_app.current_edit_set]
        _set.remove_controller(controller)

    def _open_controller_editor(self, controller_button):
        controller = controller_button.controller
        logger.info('Builder: edit {0}'.format(controller) )
        # create editor
        self.controller_editor = ControllerEditor(controller=controller, controller_button=controller_button)
        self.controller_editor.height = int(1.5 * self.button_container.button_height)
        # add editor to layout
        ix_button = self._get_controller_button_index(controller_button)
        self.button_container.container.add_widget(self.controller_editor, index=ix_button)
        # set checkboxes
        if controller.ctrl.enable:
            if controller.ctrl.is_left:
                self.controller_editor.left_ctrl_checkbox.active = True
            else:
                self.controller_editor.right_ctrl_checkbox.active = True
        if controller.shift.enable:
            if controller.shift.is_left:
                self.controller_editor.left_shift_checkbox.active = True
            else:
                self.controller_editor.right_shift_checkbox.active = True
        if controller.alt.enable:
            if controller.alt.is_left:
                self.controller_editor.left_alt_checkbox.active = True
            else:
                self.controller_editor.right_alt_checkbox.active = True
        # set editor name
        self.controller_editor.controller_name_editor.text = controller.name
        # set key
        self.controller_editor.controller_key_editor.text = controller.key

    def _close_controller_editor(self):
        controller = self.controller_editor.controller
        logger.info('Builder: close editor for {0}'.format(controller))
        # remove editor from layout
        self.button_container.remove_button(self.controller_editor)
        # reset
        self.controller_editor = None

    class DuplicateError(Exception):

        def __init__(self, info):
            self.info = info

        def __str__(self):
            return 'Duplicate {0}'.format(self.info)

    def _sync_controller_editor_to_controller(self):
        controller = self.controller_editor.controller
        # save edit to controller set
        Controller.validate_key(self.controller_editor.controller_key_editor.text)
        new_controller_name = self.controller_editor.controller_name_editor.text
        if self._exist_duplicate_controller(new_controller_name, controller):
            raise ControllerCollectionBuildScreen.DuplicateError('Controller {0}'.format(new_controller_name))
        # .. sync name
        if controller.name != new_controller_name:
            self._remove_controller_from_editing_set(controller)
            controller.name = new_controller_name
            self._add_controller_to_editing_set(controller)
        # .. sync key
        controller.key = self.controller_editor.controller_key_editor.text
        # .. sync ctrl
        if self.controller_editor.left_ctrl_checkbox.active:
            controller.ctrl.enable  = True
            controller.ctrl.is_left = True
        elif self.controller_editor.right_ctrl_checkbox.active:
            controller.ctrl.enable  = True
            controller.ctrl.is_left = False
        else:
            controller.ctrl.enable  = False
            controller.ctrl.is_left = True
        # .. sync shift
        if self.controller_editor.left_shift_checkbox.active:
            controller.shift.enable  = True
            controller.shift.is_left = True
        elif self.controller_editor.right_shift_checkbox.active:
            controller.shift.enable  = True
            controller.shift.is_left = False
        else:
            controller.shift.enable  = False
            controller.shift.is_left = True
        # .. sync alt
        if self.controller_editor.left_alt_checkbox.active:
            controller.alt.enable  = True
            controller.alt.is_left = True
        elif self.controller_editor.right_alt_checkbox.active:
            controller.alt.enable  = True
            controller.alt.is_left = False
        else:
            controller.alt.enable  = False
            controller.alt.is_left = True
        # .. sync text to controller button
        for name, value in controller.dump().items():
            text = name + '  :  ' + str(value)
        self.controller_editor.controller_button.text = text

    def _reset_controller_set_container(self):
        self.button_container.clear_buttons()

    def _get_next_new_controller_name(self):
        max_index = 0
        for controller_button in self.button_container.buttons:
            if controller_button is not self.controller_editor:
                controller_name = controller_button.controller.name
                if controller_name.startswith('New') and len(controller_name) > len('New'):
                    try:
                        max_index = int(controller_name[3:])
                        break
                    except: pass
        return 'New{0}'.format(max_index+1)

    def _get_next_new_controller_set_name(self):
        max_index = 0
        for set_name, controller_set in App.get_running_app().controller_sets.items():
            if set_name.startswith('New') and len(set_name) > len('New'):
                try:
                    max_index = max(max_index, int(set_name[3:]))
                except: pass
        return 'New{0}'.format(max_index+1)

    def _exist_duplicate_controller(self, name, controller):
        for controller_button in self.button_container.buttons:
            if name == controller_button.controller.name and controller is not controller_button.controller:
                return True
        return False

    def _exist_duplicate_controller_set(self, name, controller_set):
        for set_name, _controller_set in App.get_running_app().controller_sets.items():
            if name == set_name and controller_set is not _controller_set:
                return True
        return False

    class ControllerButtonNotFoundError(NotFoundError):

        def __int__(self, controller_button, button_container, *args):
            self.controller_button = controller_button
            self.button_container  = button_container
            super(ControllerCollectionBuildScreen.ControllerButtonNotFoundError, self).__init__(*args)

        def __str__(self):
            return ('Controller button {0} is not in button container {1}'.format(self.controller_button, self.button_container))

    def _get_controller_button_index(self, controller_button):
        for index in range(len(self.button_container.buttons)):
            if controller_button is self.button_container.buttons[index]:
                return index
        raise self.ControllerButtonNotFoundError(controller_button, self.button_container)
