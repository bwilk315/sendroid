
from    plyer       import gyroscope as gyro
from    math        import degrees
from    .sensor     import Sensor


class Gyroscope(Sensor):
    RAD_MODE    = 200
    DEG_MODE    = 201
    NO_DATA     = (.0, .0, .0)

    def __init__(self, mode: int = RAD_MODE, **kwargs) -> None:
        """
            Initializes the 'Accelerometer' class instance.
            @param mode:                Type of data gyroscope will be returning.
            @kwarg ignore_platform:     Should platform checking be omitted?
            @kwarg on_error[int, str]:  Error callback, called with the error information.
            @kwarg on_enable[]:         Method called when sensor is enabled (accessible).
            @kwarg on_disable[]:        Method called if sensor is deactivated.
        """
        self.mode       = mode
        self.on_error   = kwargs.get('on_error', lambda code, info: None)
        self.on_enable  = kwargs.get('on_enable', lambda: None)
        self.on_disable = kwargs.get('on_disable', lambda: None)
        super().__init__(
            ignore_platform=kwargs.get('ignore_platform', False),
            req_perms=[]
        )

    @property
    def rate(self) -> tuple:
        """
            Returns gyroscope rotation rate in units specified before, if gyroscope
            is unavailable returns empty tuple filled with zeroes.
        """
        try:
            rot = gyro.rotation  # Read gyroscope.
            # If gyroscope is inaccessible, None-typed tuple will be returned.
            if all(a is None for a in rot):
                return Gyroscope.NO_DATA
            # Switch gyroscope mode.
            elif self.mode == Gyroscope.RAD_MODE:
                return rot
            elif self.mode == Gyroscope.DEG_MODE:
                return (
                    degrees(rot[0]),
                    degrees(rot[1]),
                    degrees(rot[2])
                )
            else:
                return Gyroscope.NO_DATA
        except Exception as e:
            #! Program was unable to read the gyroscope data.
            self.on_error(Sensor.READ_ERROR, e)
            return self.NO_DATA

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        return True

    def _on_disable(self):
        gyro.disable()
        self.on_disable()

    def _on_enable(self):
        try:
            gyro.enable()
        except Exception as e:
            #! Program could not access the sensor to enable it.
            self.on_error(Sensor.ACCESS_ERROR, e)
        else:
            self.on_enable()

