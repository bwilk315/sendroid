
from kivy.app               import App
from kivy.lang              import Builder
from kivy.uix.boxlayout     import BoxLayout
from temp.bluetooth         import Bluetooth
from threading              import Thread
from time                   import sleep

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    Label:
        text: 'Bluetooth state'
    Label:
        id: state
        text: 'OFF'
""")


class MainLayout(BoxLayout):
    BT_INTERVAL     = .1  # Interval for next bluetooth status-readings in seconds [s].   

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Instantiate bluetooth sensor manager.
        self.bt      = Bluetooth(
            on_error    = self._on_bt_error,
            on_enable   = self._on_bt_enable,
            on_disable  = self._on_bt_disable
        )
        self.bt.set_active(True)

    def _on_bt_error(self, code: int, info: str):
        # print('>>bluetooth>> ', code, ' >> ', info)
        pass

    def _on_bt_enable(self):
        # Start bluetooth state-reading-loop.
        Thread(target = self.__app_loop).start()

    def _on_bt_disable(self):
        pass

    def __app_loop(self):
        while True:
            sleep(MainLayout.BT_INTERVAL)
            self.ids['state'].text = 'ON' if self.bt.state == Bluetooth.STATE_ON else 'OFF'
            

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MainLayout()


app = MainApp()
app.run()
