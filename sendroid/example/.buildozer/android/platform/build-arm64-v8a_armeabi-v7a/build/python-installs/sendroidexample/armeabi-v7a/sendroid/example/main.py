
from kivy.app               import App
from kivy.uix.widget        import Widget
from kivy.uix.boxlayout     import BoxLayout

from sendroid.accelerometer import Accelerometer
from sendroid.audio         import Audio
from sendroid.battery       import Battery
from sendroid.bluetooth     import Bluetooth


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio = Audio('/home/bartek/Desktop/wow.mp3')
        self.audio.record()

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def build(self) -> Widget:
        return MainLayout()


if __name__ == '__main__':
    app = MainApp()
    app.run()
