
from kivy.app           import App
from kivy.uix.widget    import Widget
from jnius              import autoclass, cast

# Everything done below is required to change brightness level since this level is a system settings and is restricted.
# Get python activity class from kivy application.
PythonActivity  = autoclass('org.kivy.android.PythonActivity')
Toast           = autoclass('android.widget.Toast')
# Cast the python activity to the common 'Activity' class in order to get its context later.
currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
# Cast got application context to the common 'Context' class to use it as actual context object.
context         = cast('android.content.Context', currentActivity.getApplicationContext())

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        toast = Toast.makeText(context, 'Ale fajne', Toast.LENGTH_LONG)
        toast.show()
        return Widget()


def run_prototype():
    MainApp().run()
