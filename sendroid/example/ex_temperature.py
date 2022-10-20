
from kivy.app               import App
from kivy.lang              import Builder
from kivy.uix.boxlayout     import BoxLayout
from threading              import Thread
from temp.temperature       import Temperature
from time                   import sleep

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    Label:
        id: temp
    Label:
        text: 'Temperature [*C]'
""")


class MainLayout(BoxLayout):
    TEM_INTERVAL    = .1  # Interval between next temperature sensor data-readings in seconds [s].

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create temperature sensor manager instance.
        self.tem            = Temperature(
            on_enable       = self._on_tem_enable,
            on_disable      = self._on_tem_disable
        )
        self.tem.set_active(True)

    def _on_tem_enable(self):
        # Start temperature data-reading-loop.
        Thread(target = self.__app_loop).start()

    def _on_tem_disable(self):
        pass

    def __app_loop(self):
        while True:
            sleep(MainLayout.TEM_INTERVAL)
            self.ids['temp'].text = str(self.tem.value)


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MainLayout()


app = MainApp()
app.run()
