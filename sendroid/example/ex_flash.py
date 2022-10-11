
from kivy.app               import App
from kivy.uix.widget        import Widget
from kivy.uix.label         import Label
from kivy.uix.button        import Button
from kivy.uix.boxlayout     import BoxLayout

from temp.flash             import Flash


class MainLayout(BoxLayout):
    FONT_SIZE       = '48px'        # Font size of all texts in the app.
    TEXT_HALIGN     = 'left'        # Text align.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation            = 'vertical'
        # Create UI elements
        self.state_label            = Label(text            = 'OFF',                font_size   = MainLayout.FONT_SIZE, halign  = MainLayout.TEXT_HALIGN)
        self.on_btn                 = Button(text           = 'Turn on',            on_release  = self.turn_on)
        self.off_btn                = Button(text           = 'Turn off',           on_release  = self.turn_off)
        self.buttons_panel          = BoxLayout(orientation = 'horizontal')
        self.on_btn.disabled        = True
        self.off_btn.disabled       = True
        # Show everything up.
        self.add_widget(self.state_label)
        self.buttons_panel.add_widget(self.on_btn)
        self.buttons_panel.add_widget(self.off_btn)
        self.add_widget(self.buttons_panel)
        # Instantiate accelerometer sensor manager.
        self.flash      = Flash(
            on_error    = self._on_flash_error,
            on_enable   = self._on_flash_enable
        )
        self.flash.set_active(True)  # Activate sensor (it may take some time).

    def turn_on(self, *largs):
        self.flash.state        = Flash.STATE_ON
        self.state_label.text   = 'ON'

    def turn_off(self, *largs):
        self.flash.state        = Flash.STATE_OFF
        self.state_label.text   = 'OFF'

    def _on_flash_error(self, code: int, info: str):
        # print('>>flasherr>>', code, '>>>(', info, ')')
        pass

    def _on_flash_enable(self):
        self.on_btn.disabled        = False
        self.off_btn.disabled       = False


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self) -> Widget:
        return MainLayout()


def run_example():
    app = MainApp()
    app.run()
