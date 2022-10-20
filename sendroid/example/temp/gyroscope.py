
from    .sensor     import Sensor
from    math        import degrees
from    plyer       import gyroscope            as gyro
from    plyer       import spatialorientation   as spato


class Gyroscope(Sensor):
    # Measurement modes.
    RAD_MODE    = 200
    DEG_MODE    = 201
    # Class-specific.
    NO_DATA     = (.0, .0, .0)

    def __init__(self, mode: int = RAD_MODE, **kwargs) -> None:
        """
            Initializes the 'Accelerometer' class instance.
            @param mode:    Type of data gyroscope will be returning.
        """
        self.mode       = mode
        super().__init__(
            # buildozer.spec: No requirements.
            req_perms=[],
            **kwargs
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
            if any(a is None for a in rot):
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

    @property
    def rotation(self) -> tuple:
        """
            Returns the actual rotation in space.
        """
        rot = spato.orientation
        if any(a is None for a in rot):
            return Gyroscope.NO_DATA
        elif self.mode == Gyroscope.DEG_MODE:
            rot = (
                degrees(rot[0]),
                degrees(rot[1]),
                degrees(rot[2])
            )
        return rot

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        return True

    def _on_disable(self):
        gyro.disable()
        spato.disable_listener()
        self.on_disable()

    def _on_enable(self):
        try:
            gyro.enable()
            spato.enable_listener()
        except Exception as e:
            #! Program could not access the sensor to enable it.
            self.on_error(Sensor.ACCESS_ERROR, e)
        else:
            self.on_enable()

