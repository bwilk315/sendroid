
from kivy.app               import App
from kivy.lang              import Builder
from kivy.uix.boxlayout     import BoxLayout
from temp.audio             import Audio

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    TextInput:
        id: sentence
        text: 'I am going to say what you input here, you can recognize this sentence to see realtime recognition.'
    Label:
        id: rec_result
        text: '[Recognition results]'
    Label:
        id: error
        text: 'No error'
    BoxLayout:
        Button:
            id: recognize
            disabled: True
            text: 'Recognize'
            on_release: root.recognize()
        Button:
            id: speak
            disabled: True
            text: 'Speak'
            on_release: root.speak()
""")


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Instantiate audio manager for STT and TTS.
        self.audio                  = Audio(
            on_error                = self._on_audio_error,
            on_enable               = self._on_audio_enable,
            on_disable              = self._on_audio_disable,
            on_speak_start          = self._on_speak_start,
            on_speak_end            = self._on_speak_end,
            on_recognize_start      = self._on_recognize_start,
            on_recognize            = self._on_recognize,
            on_recognize_end        = self._on_recognize_end
        )
        self.audio.set_active(True)

    def _on_audio_error(self, code: int, info: str):
        err = 'Unknown audio error occured'
        # If device has no specified language installed, error will occur.
        if code == Audio.LANG_ERROR:
             err = 'Language is not installed'
        # Set the error label contents.
        self.ids['error'].text = err

    def _on_audio_enable(self):
        # If device supports speech recognition enable the button for this action.
        if self.audio.speech_support:
            self.ids['recognize'].disabled = False
        self.ids['speak'].disabled = False

    def _on_audio_disable(self):
        pass

    def _on_speak_start(self):
        self.ids['speak'].disabled = True

    def _on_speak_end(self):
        self.ids['speak'].disabled = False

    def _on_recognize_start(self):
        """
            Callback invoked on speech recognition start.
        """
        self.ids['recognize'].disabled = True

    def _on_recognize(self, sentence: str):
        """
            Callback invoked every frame possible when user is speaking.
            @out sentence:  Sentence known for now (when invoked).
        """
        words = sentence.split(' ')
        for i in range(len(words)):
            # Wrap sentence every eighth word.
            if i % 8 == 0:
                words.insert(i, '\n')
        # Show recognized sentence for now in label.
        self.ids['rec_result'].text = ' '.join(words)

    def _on_recognize_end(self, matches: list):
        """
            Callback invoked when speech recognition ends (BeBeep! can be heard).
            @out matches:   List of similar sentences, first element is the most accurate.
        """
        self.ids['recognize'].disabled = False

    def speak(self, *largs):
        """
            Says the sentence inputted in a field.
        """
        self.audio.speak(self.ids['sentence'].text)

    def recognize(self, *largs):
        """
            Starts recognizing voice in english language.
        """
        self.audio.recognize(lang   = Audio.LANG_EN)


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MainLayout()


app = MainApp()
app.run()
