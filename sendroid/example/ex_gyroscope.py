
from kivy.app               import App
from kivy.uix.widget        import Widget
from kivy.uix.label         import Label
from kivy.uix.boxlayout     import BoxLayout
from threading              import Thread
from time                   import sleep

from temp.gyroscope         import Gyroscope


class MainLayout(BoxLayout):
    GYRO_INTERVAL   = .1            # Time between next gyroscope data readings.
    AXIS_FORMAT     = '{}\n{}\n{}'  # Format used to show axis values.
    FONT_SIZE       = '48px'        # Size of every text in app.
    TEXT_HALIGN     = 'left'        # Alignment of every text.
    gyro            = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation    = 'vertical'
        # Create four labels for showing data.
        self.labels         = [Label(
            font_size       = MainLayout.FONT_SIZE,
            halign          = MainLayout.TEXT_HALIGN
        ) for i in range(8)]
        # Show everything up.
        self.labels[0].text = 'Rotation rate [rad/s]'
        self.labels[2].text = 'Rotation [rad]'
        self.labels[4].text = 'Rotation rate [deg/s]'
        self.labels[6].text = 'Rotation [deg]'
        for label in self.labels:
            self.add_widget(label)
        # Instantiate gyroscope sensor manager.
        self.gyro       = Gyroscope(
            on_error    = self._on_gyro_error,
            on_enable   = self._on_gyro_enable
        )
        self.gyro.set_active(True)  # Activate sensor (it may take some time).

    def _on_gyro_error(self, code: int, info: str):
        # print('>>gyroerr>>', code, '>>>(', info, ')')
        pass

    def _on_gyro_enable(self):
        # Start the gyroscope-reading loop in another thread.
        Thread(target = self.__app_loop).start()

    def __app_loop(self):
        while True:
            sleep(MainLayout.GYRO_INTERVAL)
            # Rotation rate in radians
            self.gyro.mode      = Gyroscope.RAD_MODE
            self.labels[1].text = MainLayout.AXIS_FORMAT.format(*self.gyro.rate)
            self.labels[3].text = MainLayout.AXIS_FORMAT.format(*self.gyro.rotation)
            # Rotation rate in degrees
            self.gyro.mode      = Gyroscope.DEG_MODE  # Degrees measurement.
            self.labels[5].text = MainLayout.AXIS_FORMAT.format(*self.gyro.rate)
            self.labels[7].text = MainLayout.AXIS_FORMAT.format(*self.gyro.rotation)

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self) -> Widget:
        return MainLayout()


app = MainApp()
app.run()
