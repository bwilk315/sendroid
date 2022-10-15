
from kivy.app               import App
from kivy.uix.widget        import Widget
from kivy.uix.label         import Label
from kivy.uix.boxlayout     import BoxLayout
from threading              import Thread
from time                   import sleep

from temp.barometer         import Barometer


class MainLayout(BoxLayout):
    BAR_INTERVAL    = .1        # Interval between next barometer sensor readings in seconds [s].
    FONT_SIZE       = '48px'    # Font size of all texts in the app.
    PRES_FORMAT     = '{} hPa'   # Format for pressure displaying.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add label for showing the sensor output.
        self.value_label    = Label(
            text            = MainLayout.PRES_FORMAT.format(0),
            font_size       = MainLayout.FONT_SIZE
        )
        self.add_widget(self.value_label)
        # Create proximity sensor manager instance.
        self.bar            = Barometer(
            on_enable       = self.on_bar_enable
        )
        self.bar.set_active(True)

    def on_bar_enable(self):
        # Start reading-loop.
        Thread(target = self.__app_loop).start()

    def __app_loop(self):
        while True:
            sleep(MainLayout.BAR_INTERVAL)
            self.value_label.text = MainLayout.PRES_FORMAT.format(self.bar.pressure)

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self) -> Widget:
        return MainLayout()


app = MainApp()
app.run()
