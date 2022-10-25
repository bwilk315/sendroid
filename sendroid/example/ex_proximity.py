
from kivy.app               import App
from kivy.lang              import Builder
from kivy.uix.boxlayout     import BoxLayout
from threading              import Thread
from temp.proximity         import Proximity
from time                   import sleep

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    Label:
        id: status
    Label:
        text: 'Proximity status'
""")


class MainLayout(BoxLayout):
    PROX_INTERVAL   = .1  # Interval between next proximity sensor data-readings in seconds [s].

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create proximity sensor manager instance.
        self.prox       = Proximity(
            on_enable   = self._on_prox_enable,
            on_disable  = self._on_prox_disable
        )
        self.prox.set_active(True)

    def _on_prox_enable(self):
        # Start reading-loop.
        Thread(target = self.__app_loop).start()

    def _on_prox_disable(self):
        pass

    def __app_loop(self):
        while True:
            sleep(MainLayout.PROX_INTERVAL)
            self.ids['status'].text = 'Covered' if self.prox.covered else 'Clear'

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MainLayout()


app = MainApp()
app.run()