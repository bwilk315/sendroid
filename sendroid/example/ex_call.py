
from kivy.app               import App
from kivy.uix.widget        import Widget
from kivy.uix.label         import Label
from kivy.uix.button        import Button
from kivy.uix.textinput     import TextInput
from kivy.uix.boxlayout     import BoxLayout

from temp.call              import Call


class MainLayout(BoxLayout):
    DEF_PHONE_NUM = 000_000_000_000

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Prepare parent
        self.orientation            = 'vertical'
        # Prepare UI interface elements.
        self.phone_input            = TextInput(text        = str(MainLayout.DEF_PHONE_NUM), multiline = False)
        self.phone_input.input_type = 'tel'
        self.activity_label         = Label(text            = 'Sensor is inaccessible due to permissions :(')
        self.buttons_panel          = BoxLayout(orientation = 'horizontal')
        self.dial_btn               = Button(text           = 'Dial', on_release  = self.open_dial)
        self.call_btn               = Button(text           = 'Call', on_release  = self.make_call)
        self.phone_input.disabled   = True
        self.dial_btn.disabled      = True
        self.call_btn.disabled      = True
        # Show up UI components.
        self.add_widget(Label(text  = 'Phone number with prefix'))
        self.add_widget(self.phone_input)
        self.add_widget(self.activity_label)
        self.buttons_panel.add_widget(self.dial_btn)
        self.buttons_panel.add_widget(self.call_btn)
        self.add_widget(self.buttons_panel)
        # Create audio manager instance.
        self.call       = Call(
            on_enable   = self.on_call_enable
        )
        self.call.set_active(True)

    def on_call_enable(self):
        self.activity_label.text    = 'Sensor is available :)'
        self.phone_input.disabled   = False
        self.dial_btn.disabled      = False
        self.call_btn.disabled      = False

    def open_dial(self, *largs):
        """
            Opens the dialling interface.
        """
        self.call.dial()

    def make_call(self, *largs):
        """
            Makes a call with specified phone number.
        """
        self.call.make(int(self.phone_input.text))

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self) -> Widget:
        return MainLayout()


app = MainApp()
app.run()
