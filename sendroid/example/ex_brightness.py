
from kivy.app               import App
from kivy.lang              import Builder
from kivy.uix.boxlayout     import BoxLayout
from threading              import Thread
from temp.brightness        import Brightness
from jnius                  import autoclass, cast  # Briliant.
from time                   import sleep

# Everything done below is required to change brightness level since this level is a system settings and is restricted.
# Get python activity class from kivy application.
PythonActivity  = autoclass('org.kivy.android.PythonActivity')
# Import 'Intent', 'Settings' and 'System' class to the Python Universe.
Intent          = autoclass('android.content.Intent')
Settings        = autoclass('android.provider.Settings')
System          = autoclass('android.provider.Settings$System')
# Create special intent class instance for opening an activity for granting permissions to write system settings.
intent          = Intent()
intent.setAction(Settings.ACTION_MANAGE_WRITE_SETTINGS)
# Cast the python activity to the common 'Activity' class in order to get its context later.
currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
# Cast got application context to the common 'Context' class to use it as actual context object.
context         = cast('android.content.Context', currentActivity.getApplicationContext())

Builder.load_string(
"""
<MainLayout>:
    orientation: 'vertical'
    Button:
        text: 'Stop'
        on_release: root.stop()
    BoxLayout:
        orientation: 'horizontal'
        Button:
            text: 'Darken'
            on_release: root.darken()
        Button:
            text: 'Lighten'
            on_release: root.lighten()
""")


class MainLayout(BoxLayout):
    BRIG_INTERVAL   = .01   # Interval of next brightness changes in seconds [s].
    BRIG_CHANGE     = 1     # Value of brightness change per one interval in percent [%].

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__brig_change_dir = 0  # Direction of brightness change.
        # Instantiate brightness sensor manager.
        self.brig       = Brightness(
            on_error    = self._on_brig_error,
            on_enable   = self._on_brig_enable,
            on_disable  = self._on_brig_disable
        )
        self.brig.set_active(True)

    def _on_brig_error(self, code: int, info: str):
        # print('>>brightness>> ', code, ' >> ', info)
        pass

    def _on_brig_enable(self):
        # Start brightess-setting loop.
        Thread(target = self.__app_loop).start()

    def _on_brig_disable(self):
        pass

    def stop(self, *largs):
        self.__brig_change_dir = 0

    def lighten(self, *largs):
        self.__brig_change_dir = 1

    def darken(self, *largs):
        self.__brig_change_dir = -1

    def __app_loop(self):
        while True:
            sleep(MainLayout.BRIG_INTERVAL)
            # Change brightness level in the currently set direction.
            self.brig.level += MainLayout.BRIG_CHANGE * self.__brig_change_dir


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        # If system knows the application context can write his settings, let him go.
        if System.canWrite(context):
            return MainLayout()
        # Otherwise open panel for granting such a permission, and quit kivy application.
        else:
            currentActivity.startActivity(intent)
            self.stop()


app = MainApp()
app.run()
