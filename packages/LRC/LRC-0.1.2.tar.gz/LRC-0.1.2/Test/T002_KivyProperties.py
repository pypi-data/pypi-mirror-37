from KivyImporter import *
from random import randint

class TestWidget(Widget):

    from kivy.properties import NumericProperty

    value = NumericProperty() # this will automatically do the work to configure the events

    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)

    def on_value(self, inst, value): # "on_xx" to receive the internal event for "xx"
        print('internal for {0} {1}, is it this ? {2}'.format( inst, value, self is inst ) )


class TestMain(App):

    def build(self):
        self.inst = TestWidget()
        self.inst.bind(value=self.prop_callback)
        btn = Button(text='joker', on_press=self.change_value)
        return btn

    def prop_callback(self, inst, value):
        print('observer for {0} {1}'.format( inst, value ) )

    def change_value(self, btn):
        self.inst.value = randint(1,100)

if '__main__' == __name__:
    TestMain().run()