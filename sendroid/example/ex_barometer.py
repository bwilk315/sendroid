
from kivy.app               import App
from kivy.lang              import Builder
from kivy.uix.boxlayout     import BoxLayout
from threading              import Thread
from temp.barometer         import Barometer
from time                   import sleep

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    Label:
        id: pressure
    Label:
        text: 'Pressure [hPa]'
""")


class MainLayout(BoxLayout):
    BAR_INTERVAL    = .1  # Interval between next barometer sensor readings in seconds [s].

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Instantiate barometer sensor manager instance.
        self.bar            = Barometer(
            on_error        = self._on_bar_error,
            on_enable       = self._on_bar_enable,
            on_disable      = self._on_bar_disable
        )
        self.bar.set_active(True)

    def _on_bar_error(self, code: int, info: str):
        # print('>>barometer>> ', code, ' >> ', info)
        pass

    def _on_bar_enable(self):
        # Start barometer data-reading-loop.
        Thread(target = self.__app_loop).start()

    def _on_bar_disable(self):
        pass

    def __app_loop(self):
        while True:
            sleep(MainLayout.BAR_INTERVAL)
            self.ids['pressure'].text = str(self.bar.value)


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MainLayout()


app = MainApp()
app.run()
