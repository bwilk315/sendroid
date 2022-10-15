
from kivy.app               import App
from kivy.uix.widget        import Widget
from kivy.uix.label         import Label
from kivy.uix.boxlayout     import BoxLayout
from threading              import Thread
from time                   import sleep

from temp.proximity         import Proximity


class MainLayout(BoxLayout):
    PROX_INTERVAL   = .1        # Interval between next proximity sensor readings in seconds [s].
    FONT_SIZE       = '48px'    # Font size of all texts in the app.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add label for showing the sensor output.
        self.activity_label         = Label(
            text        = 'Sensor is inaccessible due to permissions :(',
            font_size   = MainLayout.FONT_SIZE
        )
        self.add_widget(self.activity_label)
        # Create proximity sensor manager instance.
        self.prox       = Proximity(
            on_enable   = self.on_prox_enable
        )
        self.prox.set_active(True)

    def on_prox_enable(self):
        # Start reading-loop.
        Thread(target = self.__app_loop).start()

    def __app_loop(self):
        while True:
            sleep(MainLayout.PROX_INTERVAL)
            self.activity_label.text = 'Covered' if self.prox.covered else 'Clear'

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self) -> Widget:
        return MainLayout()


app = MainApp()
app.run()
