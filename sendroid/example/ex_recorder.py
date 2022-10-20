
from kivy.app               import App
from kivy.lang              import Builder
from kivy.uix.boxlayout     import BoxLayout
from temp.audio             import Audio

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    Label:
        text: 'Output file path'
    TextInput:
        id: path
        disabled: True
        text: '/sdcard/Music/sendroid.3gp'
    Label:
        id: status
        text: 'Sensor is inaccessible'
    BoxLayout:
        orientation: 'horizontal'
        Button:
            id: record
            disabled: True
            text: 'Record'
            on_release: root.record()
        Button:
            id: finish
            disabled: True
            text: 'Finish'
            on_release: root.finish()
        Button:
            id: play
            disabled: True
            text: 'Play'
            on_release: root.play()
""")


class MainLayout(BoxLayout):
    DEF_PATH = '/sdcard/Music/sendroid.mp3'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__recorded = False  # Did player record audio already?
        # Create audio manager instance.
        self.audio      = Audio(
            data_path   = MainLayout.DEF_PATH,
            on_error    = self._on_audio_error,
            on_enable   = self._on_audio_enable,
            on_disable  = self._on_audio_disable
        )
        self.audio.set_active(True)

    def _on_audio_error(self, code: int, info: str):
        # print('>>audio>> ', code, ' >> ', info)
        pass

    def _on_audio_enable(self):
        self.ids['status']  .text       = 'Sensor is accessible'
        self.ids['path']    .disabled   = False
        self.ids['record']  .disabled   = False
        self.ids['play']    .disabled   = False

    def _on_audio_disable(self):
        pass

    def record(self, *largs):
        """
            Starts recording audio and saving data to a file on path specified before.
            @param largs:   Tuple with button object as single element.
        """
        self.__toggle_btns()
        self.audio.data_path = self.ids['path'].text
        self.audio.record()

    def finish(self, *largs):
        """
            Finishes either recording or playing audio clip.
            @param largs:   It is a tuple with only Button object inside.
        """
        self.audio.finish()
        self.__recorded = True
        self.__toggle_btns()

    def play(self, *largs):
        """
            Plays the latest audio clip recorded; note that it will not play audio file on the
            path specified.
            @param largs:   You can use its first element to get caller (Button) instance.
        """
        if self.__recorded:
            self.__toggle_btns()
            self.audio.play()

    def __toggle_btns(self):
        """
            Toggles the activity of the buttons without checking.
        """
        self.ids['record']  .disabled = not self.ids['record']  .disabled
        self.ids['finish']  .disabled = not self.ids['finish']  .disabled
        self.ids['play']    .disabled = not self.ids['play']    .disabled


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MainLayout()


app = MainApp()
app.run()
