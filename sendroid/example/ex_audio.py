
from kivy.app               import App
from kivy.uix.widget        import Widget
from kivy.uix.label         import Label
from kivy.uix.button        import Button
from kivy.uix.textinput     import TextInput
from kivy.uix.boxlayout     import BoxLayout

from temp.audio             import Audio


class MainLayout(BoxLayout):
    DEF_PATH = '/sdcard/Music/sendroid.mp3'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Prepare parent
        self.orientation            = 'vertical'
        # Prepare UI interface elements.
        self.path_input             = TextInput(text    = MainLayout.DEF_PATH, multiline = False)
        self.activity_label         = Label(text        = 'Sensor is inaccessible due to permissions :(')
        self.buttons_panel          = BoxLayout(orientation='horizontal')
        self.record_btn             = Button(text       = 'Record', on_release  = self.record)
        self.finish_btn             = Button(text       = 'Finish', on_release  = self.finish)
        self.play_btn               = Button(text       = 'Play',   on_release  = self.play)
        self.path_input.disabled    = True
        self.record_btn.disabled    = True
        self.finish_btn.disabled    = True
        self.play_btn.disabled      = True
        # Show up UI components.
        self.add_widget(Label(text  = 'Audio file path'))
        self.add_widget(self.path_input)
        self.add_widget(self.activity_label)
        self.buttons_panel.add_widget(self.record_btn)
        self.buttons_panel.add_widget(self.finish_btn)
        self.buttons_panel.add_widget(self.play_btn)
        self.add_widget(self.buttons_panel)
        # Create audio manager instance.
        self.audio      = Audio(
            data_path   = MainLayout.DEF_PATH,
            on_enable   = self.on_audio_enable
        )
        self.audio.set_active(True)

    def on_audio_enable(self):
        self.activity_label.text    = 'Sensor is available :)'
        self.path_input.disabled    = False
        self.record_btn.disabled    = False

    def record(self, *largs):
        """
            Starts recording audio and saving data to a file on path specified before, manages
            buttons' activity.
            @param largs:   Tuple with button object as single element.
        """
        self.record_btn.disabled    = True
        self.finish_btn.disabled    = False
        self.play_btn.disabled      = True
        self.audio.data_path        = self.path_input.text
        self.audio.record()

    def finish(self, *largs):
        """
            Finishes either recording or playing audio clip, manages buttons' activity.
            @param largs:   It is a tuple with only Button object inside.
        """
        self.audio.finish()
        self.record_btn.disabled    = False
        self.finish_btn.disabled    = True
        self.play_btn.disabled      = False

    def play(self, *largs):
        """
            Plays the latest audio clip recorded; note that it will not play audio file on the
            path specified.
            @param largs:   You can use its first element to get caller (Button) instance.
        """
        self.record_btn.disabled    = True
        self.finish_btn.disabled    = False
        self.play_btn.disabled      = True
        self.audio.play()

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self) -> Widget:
        return MainLayout()


app = MainApp()
app.run()
