
from kivy.app               import App
from kivy.lang              import Builder
from kivy.uix.boxlayout     import BoxLayout
from threading              import Thread
from temp.accelerometer     import Accelerometer
from time                   import sleep

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    Label:
        text: 'Full acceleration'
    Label:
        id: full
        text: '0\\n0\\n0'
    Label:
        text: 'Gravity only'
    Label:
        id: gravity
        text: '0\\n0\\n0'
    Label:
        text: 'Linear only'
    Label:
        id: linear
        text: '0\\n0\\n0'
""")


class MainLayout(BoxLayout):
    ACC_INTERVAL    = .1  # Interval between next accelerometer data-readings in seconds [s].
    AXIS_FORMAT     = '{}\n{}\n{}'

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        # Instantiate accelerometer sensor manager.
        self.acc        = Accelerometer(
            on_error    = self._on_acc_error,
            on_enable   = self._on_acc_enable,
            on_disable  = self._on_acc_disable
        )
        self.acc.set_active(True)

    def _on_acc_error(self, code: int, info: str):
        # print('>>accelerometer>> ', code, ' >> ', info)
        pass

    def _on_acc_enable(self):
        # Start accelerometer-data-reading loop to show its value.
        Thread(target = self.__app_loop).start()

    def _on_acc_disable(self):
        pass

    def __app_loop(self):
        """
            Application loop, started in different thread than main. It is used to display
            data gained from the accelerometer sensor in labels.
        """
        while True:
            sleep(MainLayout.ACC_INTERVAL) 
            self.acc.mode               = Accelerometer.FULL_MODE # Full acceleration (every acceleration included).
            self.ids['full'].text       = MainLayout.AXIS_FORMAT.format(*self.acc.data)
            self.acc.mode               = Accelerometer.GRAVITY_MODE  # Limited acceleration (only gravity).
            self.ids['gravity'].text    = MainLayout.AXIS_FORMAT.format(*self.acc.data)
            self.acc.mode               = Accelerometer.LINEAR_MODE  # Limited acceleration (only user-applied).
            self.ids['linear'].text     = MainLayout.AXIS_FORMAT.format(*self.acc.data)


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MainLayout()


app = MainApp()
app.run()
