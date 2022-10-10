
from kivy.app           import App
from kivy.uix.widget    import Widget
from jnius              import autoclass, cast

PythonActivity  = autoclass('org.kivy.android.PythonActivity')
Intent          = autoclass('android.content.Intent')
Settings        = autoclass('android.provider.Settings')
System          = autoclass('android.provider.Settings$System')

intent          = Intent()
intent.setAction(Settings.ACTION_MANAGE_WRITE_SETTINGS)

currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
context = cast('android.content.Context', currentActivity.getApplicationContext())

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        if not System.canWrite(context):
            PythonActivity.mActivity.startActivity(intent)
        return Widget()


def run_prototype():
    MainApp().run()
