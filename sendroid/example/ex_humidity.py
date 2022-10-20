
from kivy.app               import App
from kivy.lang              import Builder
from kivy.uix.boxlayout     import BoxLayout
from threading              import Thread
from temp.humidity          import Humidity
from time                   import sleep

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    Label:
        id: humidity
    Label:
        text: 'Humidity [%]'
""")


class MainLayout(BoxLayout):
    HUM_INTERVAL    = .1  # Interval between next humidity sensor readings in seconds [s].

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create humidity sensor manager instance.
        self.hum            = Humidity(
            on_enable       = self._on_hum_enable,
            on_disable      = self._on_hum_disable
        )
        self.hum.set_active(True)

    def _on_hum_enable(self):
        # Start reading-loop.
        Thread(target = self.__app_loop).start()

    def _on_hum_disable(self):
        pass

    def __app_loop(self):
        while True:
            sleep(MainLayout.HUM_INTERVAL)
            self.ids['humidity'].text = str(self.hum.value)


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MainLayout()


app = MainApp()
app.run()
