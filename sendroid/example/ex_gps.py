
from kivy.app               import App
from kivy.uix.widget        import Widget
from kivy.uix.label         import Label
from kivy.uix.boxlayout     import BoxLayout
from threading              import Thread
from time                   import sleep

from temp.gps               import GPS


class MainLayout(BoxLayout):
    FONT_SIZE       = '48px'        # Size of every text in app.
    TEXT_HALIGN     = 'left'        # Alignment of every text.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.i = 0
        self.orientation    = 'vertical'
        # Create four labels for showing data.
        self.labels         = [Label(
            font_size       = MainLayout.FONT_SIZE,
            halign          = MainLayout.TEXT_HALIGN
        ) for i in range(7)]
        # Show everything up.
        for label in self.labels:
            self.add_widget(label)
        # Instantiate gyroscope sensor manager.
        self.gps        = GPS(
            on_update   = self._on_gps_update
        )
        self.gps.set_active(True)  # Activate sensor (it may take some time).
        self._on_gps_update()  # Show the labels if gps update will not be called fast enough.
    
    def _on_gps_update(self):
        self.labels[0].text = 'Available\n{}'       .format(self.gps.available)
        self.labels[1].text = 'Latitude [deg]\n{}'  .format(self.gps.latitude)
        self.labels[2].text = 'Longitude [deg]\n{}' .format(self.gps.longitude)
        self.labels[3].text = 'Speed [m/s]\n{}'     .format(self.gps.speed)
        self.labels[4].text = 'Direction [deg]\n{}' .format(self.gps.direction)
        self.labels[5].text = 'Altitude [m]\n{}'    .format(self.gps.altitude)
        self.labels[6].text = f'Iteration {self.i}'
        self.i += 1

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self) -> Widget:
        return MainLayout()


app = MainApp()
app.run()
