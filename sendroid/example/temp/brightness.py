
from plyer      import brightness       as brig
from jnius      import autoclass, cast  # Briliant.
from .sensor    import Sensor

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


class Brightness(Sensor):
    def __init__(self, **kwargs):
        if not System.canWrite(context):
            # Open panel for granting such a permission, and quit kivy application.
            currentActivity.startActivity(intent)
        super().__init__(
            # buildozer.spec: WRITE_SETTINGS.
            req_perms = [],
            **kwargs
        )
            

    @property
    def level(self):
        return brig.current_level()

    @level.setter
    def level(self, value: int):
        # Clamp the value in proper range.
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        # Set brightness level.
        brig.set_level(value)

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        return True

    def _on_disable(self):
        self.on_disable()

    def _on_enable(self):
        self.on_enable()

