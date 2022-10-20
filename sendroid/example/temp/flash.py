
from .sensor    import Sensor
from jnius      import autoclass, cast

# Everything done below is required to change brightness level since this level is a system settings and is restricted.
# Get python activity class from kivy application.
PythonActivity  = autoclass('org.kivy.android.PythonActivity')
Camera = autoclass('android.hardware.camera2.CameraManager')
# Cast the python activity to the common 'Activity' class in order to get its context later.
currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
# Cast got application context to the common 'Context' class to use it as actual context object.
context         = cast('android.content.Context', currentActivity.getApplicationContext())


class Flash(Sensor):
    STATE_OFF   = 0
    STATE_ON    = 1

    def __init__(self, **kwargs):
        self.__state    = Flash.STATE_OFF
        self.__camera   = None
        super().__init__(
            # buildozer.spec: CAMERA, FLASHLIGHT
            req_perms   = [
                'CAMERA'
            ],
            **kwargs
        )
    
    @property
    def state(self) -> int:
        """
            Returns the current state of flash (turned on/off).
        """
        return self.__state

    @state.setter
    def state(self, value: int):
        """
            Sets the state efficiently.
        """
        if value == self.__state or not (value == Flash.STATE_OFF or value == Flash.STATE_ON):
            return
        else:
            self.__state = value
            # Use camera manager to set the torch (flash) mode of the main camera (with id equal 0).
            self.__camera.setTorchMode('0', self.__state == Flash.STATE_ON)

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        granted = all(grants)
        if granted:
            # Instance camera manager.
            self.__camera = Camera(context)
        return granted

    def _on_enable(self):
        self.on_enable()

    def _on_disable(self):
        self.on_disable()

