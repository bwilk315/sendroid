
from plyer      import vibrator as vib
from .sensor    import Sensor


class Vibrator(Sensor):
    # Time durations.
    DUR_TINY    = .1
    DUR_SHORT   = .2
    DUR_NORMAL  = .5
    DUR_LONG    = 1.5

    def __init__(self, **kwargs):
        super().__init__(
            # buildozer.spec: VIBRATE.
            req_perms = [],
            **kwargs
        )

    @property
    def exists(self) -> bool:
        """
            Returns if the device is equipped with a vibrator sensor.
        """
        return vib.exists()

    def vibrate(self, pattern: list = (.0, DUR_NORMAL), repeat: bool = False):
        """
            Vibrates using the pattern given so the first element of it is the amount
            of time to wait, next is how long vibration should occur and so on.
            @param pattern: List contatining timings which tell vibrator how to behave.
        """
        if self.exists:
            vib.pattern(pattern, 0 if repeat else -1)             

    def stop(self):
        """
            Stops the vibrator from vibrating if it is following some pattern (is active).
        """
        vib.cancel()

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        return True

    def _on_disable(self):
        self.stop()
        self.on_disable()

    def _on_enable(self):
        if self.exists:
            self.on_enable()
        else:
            #! Program was unable to access the vibrator sensor.
            self.on_error(Sensor.ACCESS_ERROR, 'Can not access vibrator; it does not exist.')

