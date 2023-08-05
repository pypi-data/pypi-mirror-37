from kivy.app import App
from kivy.uix.button import Button
import multiprocessing

class T007_App(App):

    def build(self):
        return Button(text='test', on_release=self._change)

    def _change(self, button):
        if 'test' == button.text:
            button.text = 'joke'
        elif 'joke' == button.text:
            button.text = 'test'

if '__main__' == __name__:
    multiprocessing.freeze_support() # this line solve the problem that after compilation, exe create new window again and again and again ...
    manager = multiprocessing.Manager()
    T007_App().run()