
from kivy.app               import App
from kivy.uix.widget        import Widget
from kivy.uix.label         import Label
from kivy.uix.button        import Button
from kivy.uix.textinput     import TextInput
from kivy.uix.boxlayout     import BoxLayout

from temp.audio             import Audio


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Prepare parent
        self.orientation            = 'vertical'
        # Prepare UI interface elements.
        self.text_input             = TextInput(text        = 'Text to speech. Yes', multiline  = False)
        self.words_label            = Label(text            = '[Recognized text]')
        self.error_label            = Label(text            = 'No errors.')
        self.buttons_panel          = BoxLayout(orientation = 'horizontal')
        self.speak_btn              = Button(text           = 'Speak',              on_release  = self.speak)
        self.recognize_btn          = Button(text           = 'Recognize',           on_release = self.recognize)
        self.recognize_btn.disabled = True
        # Show up UI components.
        self.add_widget(self.text_input)
        self.add_widget(self.words_label)
        self.add_widget(self.error_label)
        self.buttons_panel.add_widget(self.speak_btn)
        self.buttons_panel.add_widget(self.recognize_btn)
        self.add_widget(self.buttons_panel)
        # Instantiate audio manager for STT and TTS.
        self.audio                  = Audio(
            on_error                = self._on_audio_error,
            on_enable               = self._on_audio_enable,
            on_recognize_start      = self._on_recognize_start,
            on_recognize_end        = self._on_recognize_end
        )
        self.audio.set_active(True)  # Activate the audio sensor.

    def speak(self, *largs):
        """
            Says the sentence inputted in a field.
        """
        self.audio.speak(self.text_input.text)

    def recognize(self, *largs):
        """
            Starts recognizing voice in english language.
        """
        self.audio.recognize(lang   = Audio.LANG_EN)

    def _on_audio_error(self, code: int, info: str):
        # If device has no specified language installed, error will occur.
        if code == Audio.LANG_ERROR:
            self.error_label.text = 'Language is not installed :('

    def _on_audio_enable(self):
        if self.audio.speech_support:
            self.recognize_btn.disabled = False

    def _on_recognize_start(self):
        self.recognize_btn.disabled = True

    def _on_recognize_end(self):
        if len(self.audio.results):
            self.words_label.text = str(self.audio.results[0])
        self.recognize_btn.disabled = False

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self) -> Widget:
        return MainLayout()


app = MainApp()
app.run()
