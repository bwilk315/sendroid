
from kivy.app               import App
from kivy.lang              import Builder
from kivy.uix.boxlayout     import BoxLayout
from threading              import Thread
from temp.battery           import Battery
from time                   import sleep

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    Label:
        text: 'Filling percent'
    Label:
        id: percent
        text: '0'
    Label:
        text: 'Is battery charging?'
    Label:
        id: state
        text: 'No'
""")


class MainLayout(BoxLayout):
    BAT_INTERVAL    = .1  # Time between next battery data-readings in seconds [s].

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Instantiate battery sensor manager.
        self.bat            = Battery(
            on_error        = self._on_bat_error,
            on_enable       = self._on_bat_enable,
            on_disable      = self._on_bat_disable
        )
        self.bat.set_active(True)

    def _on_bat_error(self, code: int, info: str):
        # print('>>battery>> ', code, ' >> ', info)
        pass

    def _on_bat_enable(self):
        # Start the battery-reading loop in another thread.
        Thread(target = self.__app_loop).start()

    def _on_bat_disable(self):
        pass

    def __app_loop(self):
        while True:
            sleep(MainLayout.BAT_INTERVAL)
            self.ids['percent'] .text   = str(self.bat.percent)
            self.ids['state']   .text   = 'Yes' if self.bat.charging else 'No'


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MainLayout()


app = MainApp()
app.run()
