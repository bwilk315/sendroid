
from    .sensor         import Sensor
from    plyer           import accelerometer    as acc
from    plyer           import gravity          as grav


class Accelerometer(Sensor):
    # Errors.
    MODE_ERROR      = 100
    # Modes.
    FULL_MODE       = 200
    GRAVITY_MODE    = 201
    LINEAR_MODE     = 202
    # Class specific.
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
                #! Program does not know the mode specified.
                self.on_error(Accelerometer.MODE_ERROR, f'Unknown accelerometer mode {self.mode}.')
                return Accelerometer.NO_DATA
            # If any axis value is None then its value is inaccessible, return empty tuple
            if any(a is None for a in acc_val):
                return Accelerometer.NO_DATA
        except:
            #! Program was unable to read sensor data due to exception.
            self.on_error(Accelerometer.READ_ERROR, 'Error occurred when tried to read the data.')
            return Accelerometer.NO_DATA
        else:
            return acc_val

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        return True

    def _on_enable(self):
        x = 1
        try:
            acc.enable()
            x = 0
            grav.enable()
        except:
            obj = 'accelerometer sensor.' if x else 'both accelerometer and gravity.'
            #! Program could not access the sensors in order to enable it.
            self.error(Accelerometer.ACCESS_ERROR, f'Can not access {obj}.')
        else:
            self.on_enable()

    def _on_disable(self):
        # Disable sensors.
        acc.disable()
        grav.disable()
        self.on_disable()

