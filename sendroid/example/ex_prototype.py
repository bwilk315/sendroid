
from kivy.app           import App
from kivy.uix.widget    import Widget
from jnius              import autoclass

System  = autoclass('java.lang.System')

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        System.out.println('Co ja tu robie')
        return Widget()


def run_prototype():
    MainApp().run()
