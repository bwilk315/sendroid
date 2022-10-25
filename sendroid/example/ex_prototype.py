
from kivy.app           import App
from kivy.lang          import Builder
from kivy.uix.boxlayout import BoxLayout
from temp.bridge        import Bridge, JSensor, JSensorManager, Sensor
from threading          import Thread
from time               import sleep

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    Label:
        id: label
""")


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        bridge = Bridge()
        total = len(bridge.device_sensors)
        self.ids['label'].text = f'Supported sensors ({total}):' + ('\n{}' * total).format(*bridge.device_sensors)
        # self.cusensor = Sensor(JSensor.TYPE_LINEAR_ACCELERATION, JSensorManager.SENSOR_DELAY_NORMAL)
        # self.cusensor.start()
        # Thread(target = self.__app_loop).start()

    def __del__(self):
        self.cusensor.stop()

    def __app_loop(self):
        while True:
            sleep(.01)
            values = self.cusensor.data
            self.ids['label'].text = '\n'.join(str(values)[1:-1].split(',')) if len(values) else 'No data!'


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MainLayout()


app = MainApp()
app.run()
