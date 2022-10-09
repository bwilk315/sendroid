
from kivy.app               import App
from kivy.uix.widget        import Widget
from kivy.uix.label         import Label
from kivy.uix.boxlayout     import BoxLayout
from threading              import Thread

from temp.accelerometer     import Accelerometer


class MainLayout(BoxLayout):
    ACC_INTERVAL    = 64                # Number of interval frames (these between next sensor readings).
    AXIS_FORMAT     = '{}\n{}\n{}\n{}'  # Format used to show accelerometer axis values.
    FONT_SIZE       = '48px'            # Font size of all texts in the app.
    TEXT_HALIGN     = 'left'            # Text align.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation    = 'vertical'
        # Create labels for showing data.
        self.labels         = [Label(
            font_size       = MainLayout.FONT_SIZE,
            halign          = MainLayout.TEXT_HALIGN
        ) for i in range(3)]
        # Show everything up.
        for label in self.labels:
            self.add_widget(label)
        # Instantiate accelerometer sensor manager.
        self.acc        = Accelerometer(
            on_error    = self._on_acc_error,
            on_enable   = self._on_acc_enable
        )
        self.acc.set_active(True)  # Activate sensor (it may take some time).
        self._frame = 0  # Current frame index.

    def _on_acc_error(self, code: int, info: str):
        # print('>>accerr>>', code, '>>>(', info, ')')
        pass

    def _on_acc_enable(self):
        # Start accelerometer-data-reading loop to show its value.
        Thread(target = self.__app_loop).start()

    def __app_loop(self):
        """
            Application loop, started in different thread than main. It is used to display
            data gained from the accelerometer sensor in labels.
        """
        while True:
            if not self._frame % MainLayout.ACC_INTERVAL:
                self.acc.mode       = Accelerometer.FULL_MODE # Full acceleration (every acceleration included).
                self.labels[0].text = MainLayout.AXIS_FORMAT.format('Full [m/s^2]', *self.acc.data)
                self.acc.mode       = Accelerometer.GRAVITY_MODE  # Limited acceleration (only gravity).
                self.labels[1].text = MainLayout.AXIS_FORMAT.format('Gravity [m/s^2]', *self.acc.data)
                self.acc.mode       = Accelerometer.LINEAR_MODE  # Limited acceleration (only user-applied).
                self.labels[2].text = MainLayout.AXIS_FORMAT.format('Linear [m/s^2] ', *self.acc.data)
            self._frame += 1


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self) -> Widget:
        return MainLayout()


def run_example():
    app = MainApp()
    app.run()
