
from kivy.app               import App
from kivy.uix.widget        import Widget
from kivy.uix.label         import Label
from kivy.uix.boxlayout     import BoxLayout

from temp.bluetooth         import Bluetooth


class MainLayout(BoxLayout):
    BT_INTERVAL     = .1        # Interval for next bluetooth status readings.   
    FONT_SIZE       = '48px'    # Font size of all texts in the app.
    TEXT_HALIGN     = 'left'    # Text align.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create UI element for showing the bluetooth status.
        self.state_label            = Label(font_size = MainLayout.FONT_SIZE, halign = MainLayout.TEXT_HALIGN)
        # Show everything up.
        self.add_widget(self.state_label)
        # Instantiate bluetooth sensor manager.
        self.bt      = Bluetooth(
            on_error    = self._on_bt_error,
            on_enable   = self._on_bt_enable
        )
        self.bt.set_active(True)  # Activate sensor (it may take some time).

    def _on_bt_error(self, code: int, info: str):
        # print('>>bterr>>', code, '>>>(', info, ')')
        pass

    def _on_bt_enable(self):
        self.state_label.text = 'Bluetooth is ON' if self.bt.state == Bluetooth.STATE_ON else 'Bluetooth is OFF'

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self) -> Widget:
        return MainLayout()


app = MainApp()
app.run()
