
from kivy.app               import App
from kivy.uix.widget        import Widget
from kivy.uix.label         import Label
from kivy.uix.boxlayout     import BoxLayout
from kivy.uix.button        import Button
from threading              import Thread
from time                   import sleep, time
from math                   import degrees

from temp.gyroscope         import Gyroscope


class MainLayout(BoxLayout):
    GYRO_DELTA      = 0.1  # Time between next gyroscope data readings.
    AXIS_FORMAT     = '{}\n{}\n{}\n{}'  # Format used to show axis values.
    FONT_SIZE       = '48px'  # Size of every text in app.
    TEXT_HALIGN     = 'left'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation    = 'vertical'
        # Create four labels for showing data.
        self.labels         = [Label(
            font_size       = MainLayout.FONT_SIZE,
            halign          = MainLayout.TEXT_HALIGN
        ) for i in range(2)]
        # Show everything up.
        for label in self.labels:
            self.add_widget(label)
        # Instantiate gyroscope sensor manager.
        self.gyro = Gyroscope(
            on_enable=self._on_gyro_enable,
            on_error=self._on_gyro_error
        )
        self.gyro.set_active(True)  # Activate sensor (it may take some time).

    def _on_gyro_error(self, code: int, info: str):
        # print('>>gyroerr>>', code, '>>>(', info, ')')
        pass

    def _on_gyro_enable(self):
        # Start the gyroscope-reading loop in another thread.
        Thread(target=self.__app_loop).start()

    def __app_loop(self):
        while True:
            sleep(MainLayout.GYRO_DELTA)
            # Rotation in radians
            self.gyro.mode      = Gyroscope.RAD_MODE
            self.labels[0].text = MainLayout.AXIS_FORMAT.format('Rate of rotation [rad/s]', *self.gyro.rate)
            # Rotation in degrees
            self.gyro.mode      = Gyroscope.DEG_MODE  # Degrees measurement.
            self.labels[1].text = MainLayout.AXIS_FORMAT.format('Rate of rotation [deg/s]', *self.gyro.rate)

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self) -> Widget:
        return MainLayout()


def run_example():
    app = MainApp()
    app.run()
