
from kivy.app               import App
from kivy.lang              import Builder
from kivy.uix.boxlayout     import BoxLayout
from temp.call              import Call

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    Label:
        text: 'Phone number'
    TextInput:
        id: phone
        disabled: True
        input_type: 'tel'
        text: '000000000000'
    Label:
        id: status
        text: 'Sensor is inaccessible'
    BoxLayout:
        orientation: 'horizontal'
        Button:
            id: dial
            disabled: True
            text: 'Dial'
            on_release: root.open_dial()
        Button:
            id: call
            disabled: True
            text: 'Call'
            on_release: root.make_call()
""")


class MainLayout(BoxLayout):
    DEF_PHONE_NUM = 000_000_000_000

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create calling manager instance.
        self.call       = Call(
            on_error    = self._on_call_error,
            on_enable   = self._on_call_enable,
            on_disable  = self._on_call_disable
        )
        self.call.set_active(True)

    def _on_call_error(self, code: int, info: str):
        # print('>>call>> ', code, ' >> ', info)
        pass

    def _on_call_enable(self):
        self.ids['status']  .text       = 'Sensor is accessible'
        self.ids['phone']   .disabled   = False
        self.ids['dial']    .disabled   = False
        self.ids['call']    .disabled   = False

    def _on_call_disable(self):
        pass

    def open_dial(self, *largs):
        """
            Opens the dialling interface.
        """
        self.call.dial()

    def make_call(self, *largs):
        """
            Makes a call with specified phone number if it is valid.
        """
        phone_str = self.ids['phone'].text  # Get inputted phone number.
        # Check the number and perform proper action.
        num = int(phone_str) if len(phone_str) else MainLayout.DEF_PHONE_NUM
        self.call.make(num)


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MainLayout()


app = MainApp()
app.run()
