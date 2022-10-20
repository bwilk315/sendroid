
from kivy.app               import App
from kivy.lang              import Builder
from kivy.uix.boxlayout     import BoxLayout
from threading              import Thread
from temp.gyroscope         import Gyroscope
from time                   import sleep

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    Label:
        text: 'Rotation rate [rad/s]'
    Label:
        id: rate_rad
        text: '0.0\\n0.0\\n0.0'
    Label:
        text: 'Rotation [rad]'
    Label:
        id: rot_rad
        text: '0.0\\n0.0\\n0.0'
    Label:
        text: 'Rotation rate [deg/s]'
    Label:
        id: rate_deg
        text: '0.0\\n0.0\\n0.0'
    Label:
        text: 'Rotation [deg]'
    Label:
        id: rot_deg
        text: '0.0\\n0.0\\n0.0'
""")


class MainLayout(BoxLayout):
    GYRO_INTERVAL   = .1            # Time between next gyroscope data readings.
    AXIS_FORMAT     = '{}\n{}\n{}'  # Format used to show axis values.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Instantiate gyroscope sensor manager.
        self.gyro       = Gyroscope(
            on_error    = self._on_gyro_error,
            on_enable   = self._on_gyro_enable,
            on_disable  = self._on_gyro_disable
        )
        self.gyro.set_active(True)

    def _on_gyro_error(self, code: int, info: str):
        # print('>>gyroscope>> ', code, ' >> ', info)
        pass

    def _on_gyro_enable(self):
        # Start the gyroscope-reading loop in another thread.
        Thread(target = self.__app_loop).start()

    def _on_gyro_disable(self):
        pass

    def __app_loop(self):
        while True:
            sleep(MainLayout.GYRO_INTERVAL)
            # Rotation rate in radians.
            self.gyro.mode              = Gyroscope.RAD_MODE
            self.ids['rate_rad'].text   = MainLayout.AXIS_FORMAT.format(*self.gyro.rate)
            self.ids['rot_rad'] .text   = MainLayout.AXIS_FORMAT.format(*self.gyro.rotation)
            # Rotation rate in degrees.
            self.gyro.mode              = Gyroscope.DEG_MODE
            self.ids['rate_deg'].text   = MainLayout.AXIS_FORMAT.format(*self.gyro.rate)
            self.ids['rot_deg'] .text   = MainLayout.AXIS_FORMAT.format(*self.gyro.rotation)


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MainLayout()


app = MainApp()
app.run()
