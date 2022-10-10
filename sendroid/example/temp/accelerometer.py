
from    plyer           import accelerometer    as acc
from    plyer           import gravity          as grav
from    .sensor         import Sensor


class Accelerometer(Sensor):
    # Errors.
    MODE_ERROR      = 100
    # Modes.
    FULL_MODE       = 200
    GRAVITY_MODE    = 201
    LINEAR_MODE     = 202
    # Class specific.
    GRAVITY         = 9.81
    NO_DATA         = (.0, .0, .0)

    def __init__(self, mode: int = FULL_MODE, **kwargs):
        """
            Initializes the 'Accelerometer' class instance.
            @param mode:    Type of functionality accelerometer will perform.
        """
        self.mode       = mode
        super().__init__(
            # buildozer.spec: No requirements.
            req_perms   = [],
            **kwargs
        )

    @property
    def data(self) -> tuple:
        """
            Returns the value of accelerometer sensor. The data returned consists of
            three values (x, y and z) which represent the acceleration in mode specified before.
        """
        try:
            if self.mode == Accelerometer.FULL_MODE:
                acc_val = acc.acceleration
            elif self.mode == Accelerometer.GRAVITY_MODE:
                acc_val = grav.gravity
            elif self.mode == Accelerometer.LINEAR_MODE:
                # TODO: Implement linear acceleration
                acc_val = Accelerometer.NO_DATA
            else:
                self.on_error(Accelerometer.MODE_ERROR)
                return Accelerometer.NO_DATA
            # If any axis value is None then its value is inaccessible, return empty tuple
            if any(a is None for a in acc_val):
                return Accelerometer.NO_DATA
        except:
            #! Program was unable to read sensor data due to exception.
            self.on_error(Accelerometer.READ_ERROR)
            return Accelerometer.NO_DATA
        else:
            return acc_val

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        return True

    def _on_disable(self):
        acc.disable()
        grav.disable()
        self.on_disable()

    def _on_enable(self):
        try:
            acc.enable()
            grav.enable()
        except:
            #! Program could not access the sensor to enable it.
            self.error = Accelerometer.ACCESS_ERROR
        else:
            self.on_enable()

