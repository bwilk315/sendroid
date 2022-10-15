
from kivy.app               import App
from kivy.uix.widget        import Widget
from kivy.uix.label         import Label
from kivy.uix.boxlayout     import BoxLayout
from threading              import Thread

from temp.battery           import Battery


class MainLayout(BoxLayout):
    BAT_INTERVAL    = 1024      # Time between next battery data readings (here one kiloframe [kf]).
    FONT_SIZE       = '48px'    # Size of every text in app.
    TEXT_HALIGN     = 'left'    # Alignment of every text.
    frame           = 0         # Index of the current frame, used to limit readings.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation    = 'vertical'
        # Create four labels for showing data.
        self.labels         = [Label(
            font_size       = MainLayout.FONT_SIZE,
            halign          = MainLayout.TEXT_HALIGN
        ) for i in range(4)]
        # Show everything up.
        self.labels[0].text = 'Battery filling percent'
        self.labels[2].text = 'Is battery in charging state?'
        for label in self.labels:
            self.add_widget(label)
        # Instantiate battery sensor manager.
        self.bat            = Battery(
            on_error        = self._on_bat_error,
            on_enable       = self._on_bat_enable
        )
        self.bat.set_active(True)  # Activate sensor (it may take some time).

    def _on_bat_error(self, code: int, info: str):
        # print('>>baterr>>', code, '>>>(', info, ')')
        pass

    def _on_bat_enable(self):
        # Start the battery-reading loop in another thread.
        Thread(target = self.__app_loop).start()

    def __app_loop(self):
        while True:
            if not MainLayout.frame % MainLayout.BAT_INTERVAL:
                # Show the percent of battery filling.
                self.labels[1].text = str(self.bat.percent)
                # Show whether battery is in charging state.
                self.labels[3].text = str(self.bat.charging)
            MainLayout.frame += 1

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self) -> Widget:
        return MainLayout()


app = MainApp()
app.run()
