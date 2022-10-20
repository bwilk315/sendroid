
from kivy.app               import App
from kivy.lang              import Builder
from kivy.uix.boxlayout     import BoxLayout
from temp.flash             import Flash

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    Label:
        id: status
        text: 'OFF or ON'
    BoxLayout:
        orientation: 'horizontal'
        Button:
            id: on
            disabled: True
            text: 'Turn on'
            on_release: root.turn_on()
        Button:
            id: off
            disabled: True
            text: 'Turn off'
            on_release: root.turn_off()
""")


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Instantiate flash sensor manager.
        self.flash      = Flash(
            on_error    = self._on_flash_error,
            on_enable   = self._on_flash_enable,
            on_disable  = self._on_flash_disable
        )
        self.flash.set_active(True)

    def _on_flash_error(self, code: int, info: str):
        # print('>>flash>> ', code, ' >> ', info)
        pass

    def _on_flash_enable(self):
        self.ids['on']  .disabled   = False
        self.ids['off'] .disabled   = False

    def _on_flash_disable(self):
        pass

    def turn_on(self, *largs):
        self.flash.state        = Flash.STATE_ON
        self.ids['status'].text = 'ON'

    def turn_off(self, *largs):
        self.flash.state        = Flash.STATE_OFF
        self.ids['status'].text = 'OFF'


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MainLayout()


app = MainApp()
app.run()
