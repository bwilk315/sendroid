
from kivy.app               import App
from kivy.lang              import Builder
from kivy.uix.boxlayout     import BoxLayout
from temp.vibrator          import Vibrator

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    Label:
        id: status
        text: 'Sensor is inaccessible'
    BoxLayout:
        orientation: 'horizontal'
        Button:
            id: vibrate
            disabled: True
            text: 'Vibrate'
            on_release: root.vibrate()
        Button:
            id: rickroll
            disabled: True
            text: 'Rickroll'
            on_release: root.rickroll()
    Button:
        id: stop
        disabled: True
        text: 'Stop'
        on_release: root.stop()
""")


class MainLayout(BoxLayout):
    # "Never gonna give you up" vibrator pattern.
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
        # Create vibrator sensor manager instance.
        self.vib      = Vibrator(
            on_enable   = self.on_vib_enable,
            on_disable  = self._on_vib_disable
        )
        self.vib.set_active(True)

    def on_vib_enable(self):
        self.ids['status']  .text       = 'Sensor is accessible'
        self.ids['vibrate'] .disabled   = False
        self.ids['rickroll'].disabled   = False
        self.ids['stop']    .disabled   = False

    def _on_vib_disable(self):
        pass

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
            Plays the "Never gonna give you up" song (by Rick Astley) using the vibrator.
        """
        self.vib.vibrate(
            pattern = MainLayout.PAT_NGGYU,
            repeat  = True
        )

    def stop(self, *largs):
        """
            Stops the vibration process (current vibration sensor job).
        """
        self.vib.stop()


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MainLayout()


app = MainApp()
app.run()
