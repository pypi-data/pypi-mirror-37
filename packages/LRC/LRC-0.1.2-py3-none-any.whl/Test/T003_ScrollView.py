from KivyImporter import *

Builder.load_string('''
<ScreenA>:
    Button:
        text: 'screen A'
        on_press: root.to_b()
        size_hint: 0.3, 0.3
        pos_hint: {'x':0, 'y':0}

<ScreenB>:
    Button:
        text: 'screen B'
        on_press: root.to_a()
        size_hint: 0.3, 0.3
        pos_hint: {'x':0.7, 'y':0.7}
''')


class ScreenA(Screen):

    def to_b(self):
        print('to b by', self.manager)
        self.manager.current = "B"

    pass

class ScreenB(Screen):

    def to_a(self):
        print('to a by', self.manager)
        self.manager.current  = "A"

    pass

class BuildWithScreen(App):

    def build(self):
        manager = ScreenManager()

        manager.add_widget(ScreenA(name="A"))

        manager.add_widget(ScreenB(name="B"))

        manager.current  = "B"
        self.screen_manager = manager
        return manager



    pass


class Directly(App):

    def build(self):
        root = BoxLayout(orientation='vertical', padding=30, spacing=10)
        root.add_widget(Button(text='add', size_hint=(0.6,0.1), pos_hint={'center_x':0.5, 'center_y':0.5},
                               on_press=self.add_button))

        scroll = ScrollView()
        root.add_widget(scroll)

        layout = BoxLayout(orientation='vertical', size_hint=(1,None))
        scroll.add_widget(layout)

        layout.bind(minimum_height=layout.setter('height'))

        self.index = 7
        for i in range(self.index):
            text = 'joker {0}'.format(i)
            layout.add_widget(Button(text=text, size_hint=(1,None), height=60))

        self.scroll_layout = layout
        return root

    def on_start(self):
        pass

    def add_button(self, _):
        self.index += 1
        text = 'joker {0}'.format(self.index)
        self.scroll_layout.add_widget(Button(text=text, size_hint=(1,None), height=60))

def _test000_directly_build_scroll_view_in_app():
    Directly().run()


def _test001_build_scroll_view_with_screens():
    BuildWithScreen().run()

if '__main__' == __name__:
    # _test000_directly_build_scroll_view_in_app()
    _test001_build_scroll_view_with_screens()