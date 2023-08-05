# -*-coding:utf-8-*-
from __future__ import print_function

import kivy
# kivy.require('1.9.1')
try: # python 2
    from kivy.app import App
    from kivy.uix.button import Button
    from kivy.uix.widget import Widget
    from kivy.uix.gridlayout import GridLayout
except ImportError: # python 3
    from kivy.app import App
    from kivy.uix.button import Button
    from kivy.uix.widget import Widget
    from kivy.uix.GridLayout import GridLayout
except:
    print('can not import packages for T001_UsingKivy')
finally:
    pass

class HelloWorld( App ):
    def build(self):
        return Button(text='hello world')

def test000():
    HelloWorld().run()


class MultiButton( GridLayout ):
    def __init__(self, **kwargs):
        super(MultiButton, self).__init__(**kwargs)
        self.rows = 2
        self.add_widget( Button(text='one') )
        self.add_widget( Button(text='two') )
        pass

class test(App):
    def build(self):
        return MultiButton()

def test001():
    test().run()

if __name__ == '__main__':
    test001()
    pass




