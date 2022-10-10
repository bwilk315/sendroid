
from kivy.app               import App
from kivy.uix.widget        import Widget
from kivy.uix.label         import Label
from kivy.uix.button        import Button
from kivy.uix.boxlayout     import BoxLayout

from temp.vibrator          import Vibrator


class MainLayout(BoxLayout):
    # Vibrator patterns.
    PAT_NGGYU = (
        .0,                     Vibrator.DUR_NORMAL,
        Vibrator.DUR_SHORT,     Vibrator.DUR_NORMAL,
        Vibrator.DUR_SHORT,     Vibrator.DUR_SHORT,
        Vibrator.DUR_SHORT,     Vibrator.DUR_NORMAL,
        Vibrator.DUR_SHORT,     Vibrator.DUR_NORMAL,
        Vibrator.DUR_TINY,      Vibrator.DUR_TINY,
        Vibrator.DUR_TINY,      Vibrator.DUR_TINY,
        Vibrator.DUR_TINY,      Vibrator.DUR_TINY,
        Vibrator.DUR_TINY,      .0
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Prepare parent
        self.orientation            = 'vertical'
        # Prepare UI interface elements.
        self.activity_label         = Label(text            = 'You do not have vibrator :(')
        self.buttons_panel          = BoxLayout(orientation ='horizontal')
        self.stop_btn               = Button(text           = 'Stop',       on_release = self.stop)
        self.stop_btn.disabled      = True
        self.vibrate_btn            = Button(text           = 'Vibrate',    on_release = self.vibrate)
        self.vibrate_btn.disabled   = True
        self.rickroll_btn           = Button(text           = 'Rickroll',   on_release = self.rickroll)
        self.rickroll_btn.disabled  = True
        # Show up UI components.
        self.add_widget(self.activity_label)
        self.buttons_panel.add_widget(self.vibrate_btn)
        self.buttons_panel.add_widget(self.rickroll_btn)
        self.add_widget(self.buttons_panel)
        self.add_widget(self.stop_btn)
        # Create vibrator sensor manager instance.
        self.vib      = Vibrator(
            on_enable   = self.on_vib_enable
        )
        self.vib.set_active(True)

    def on_vib_enable(self):
        self.activity_label.text    = 'Have fun with the vibrator!'
        self.stop_btn.disabled      = False
        self.vibrate_btn.disabled   = False
        self.rickroll_btn.disabled  = False

    def vibrate(self, *largs):
        """
            Uses vibrator sensor to vibrate for a normal period of time.
        """
        self.vib.vibrate(
            pattern = (.0, Vibrator.DUR_LONG),
            repeat  = False
        )

    def rickroll(self, *largs):
        """
            Plays the "Never gonna give you up" song (Rick Astley) using the vibrator.
        """
        self.vib.vibrate(
            pattern = MainLayout.PAT_NGGYU,
            repeat  = True
        )

    def stop(self, *largs):
        """
            Stops the vibration process (vibrator sensor job).
        """
        self.vib.stop()

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self) -> Widget:
        return MainLayout()

def run_example():
    app = MainApp()
    app.run()
