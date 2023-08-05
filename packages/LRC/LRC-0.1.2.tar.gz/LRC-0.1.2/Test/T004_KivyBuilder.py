from KivyImporter import *

Builder.load_string('''
<Test>:
    Button:
        text: 'test'
''')


class Test(Widget): # rules can be build only for widget, App can not load by kv string

    pass

class Main(App):

    def build(self):
        return Test()

    pass

if '__main__' == __name__:
    Main().run()