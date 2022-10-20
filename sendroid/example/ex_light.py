
from kivy.app               import App
from kivy.lang              import Builder
from kivy.uix.boxlayout     import BoxLayout
from threading              import Thread
from temp.light             import Light
from time                   import sleep

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    Label:
        id: light
    Label:
        text: 'Light [lx]'
""")


class MainLayout(BoxLayout):
    LIG_INTERVAL    = .1  # Interval between next light data-readings in seconds [s].

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Instantiate light sensor manager.
        self.lig        = Light(
            on_error    = self._on_lig_error,
            on_enable   = self._on_lig_enable,
            on_disable  = self._on_lig_disable
        )
        self.lig.set_active(True)

    def _on_lig_error(self, code: int, info: str):
        # print('>>light>> ', code, ' >> ', info)
        pass

    def _on_lig_enable(self):
        # Start accelerometer-data-reading loop to show its value.
        Thread(target = self.__app_loop).start()

    def _on_lig_disable(self):
        pass

    def __app_loop(self):
        while True:
            sleep(MainLayout.LIG_INTERVAL)
            self.ids['light'].text = str(self.lig.value)


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MainLayout()


app = MainApp()
app.run()
