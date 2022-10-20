
from kivy.app               import App
from kivy.lang              import Builder
from kivy.uix.boxlayout     import BoxLayout
from temp.gps               import Gps

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    Label:
        text: 'Available'
    Label:
        id: status
        text: 'False'
    Label:
        text: 'Latitude [deg]'
    Label:
        id: lat
        text: '0.0'
    Label:
        text: 'Longitude [deg]'
    Label:
        id: lon
        text: '0.0'
    Label:
        text: 'Speed [m/s]'
    Label:
        id: speed
        text: '0.0'
    Label:
        text: 'Direction [deg]'
    Label:
        id: dir
        text: '0.0'
    Label:
        text: 'Altitude [m]'
    Label:
        id: alt
        text: '0.0'
""")


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Instantiate gps sensor manager.
        self.gps        = Gps(
            on_update   = self._on_gps_update,
            on_enable   = self._on_gps_enable,
            on_disable  = self._on_gps_disable
        )
        self.gps.set_active(True)
    
    def _on_gps_enable(self):
        pass

    def _on_gps_disable(self):
        pass

    def _on_gps_update(self, status: bool):
        self.ids['status'].text = str(status)
        if status:
            self.ids['lat']     .text = str(self.gps.latitude)
            self.ids['lon']     .text = str(self.gps.longitude)
            self.ids['speed']   .text = str(self.gps.speed)
            self.ids['dir']     .text = str(self.gps.direction)
            self.ids['alt']     .text = str(self.gps.altitude)


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MainLayout()


app = MainApp()
app.run()
