
from kivy.app               import App
from kivy.uix.widget        import Widget
from kivy.uix.label         import Label
from kivy.uix.boxlayout     import BoxLayout
from threading              import Thread
from time                   import sleep

from temp.light             import Light


class MainLayout(BoxLayout):
    ACC_INTERVAL    = .1            # Number of interval frames (these between next sensor readings).
    AXIS_FORMAT     = '{}\n{}\n{}'  # Format used to show accelerometer axis values.
    FONT_SIZE       = '48px'        # Font size of all texts in the app.
    TEXT_HALIGN     = 'left'        # Text align.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation    = 'vertical'
        # Create labels for showing data.
        self.labels         = [Label(
            font_size       = MainLayout.FONT_SIZE,
            halign          = MainLayout.TEXT_HALIGN
        ) for i in range(2)]
        # Show everything up.
        self.labels[0].text = 'Illumination [lx]'
        for label in self.labels:
            self.add_widget(label)
        # Instantiate accelerometer sensor manager.
        self.lig        = Light(
            on_error    = self._on_lig_error,
            on_enable   = self._on_lig_enable
        )
        self.lig.set_active(True)  # Activate sensor (it may take some time).

    def _on_lig_error(self, code: int, info: str):
        # print('>>ligerr>>', code, '>>>(', info, ')')
        pass

    def _on_lig_enable(self):
        # Start accelerometer-data-reading loop to show its value.
        Thread(target = self.__app_loop).start()

    def __app_loop(self):
        """
            Application loop, started in different thread than main. It is used to display
            data gained from the accelerometer sensor in labels.
        """
        while True:
            sleep(MainLayout.ACC_INTERVAL)
            self.labels[1].text = str(self.lig.value)


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self) -> Widget:
        return MainLayout()


def run_example():
    app = MainApp()
    app.run()
