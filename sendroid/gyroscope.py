
from    plyer      import gyroscope
from    math       import degrees
from    .sensor     import Sensor
import  logging


class Gyroscope(Sensor):
    """
        Management class for gyroscope sensor.
    """
    NO_GYRO_VALUE = (.0, .0, .0)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def on_disable(self) -> None:
        gyroscope.disable()

    def on_enable(self) -> None:
        try:
            gyroscope.enable()
        except Exception as e:
            logging.error('Failed to enable the gyroscope on device: %s', e)
            return False
        else:
            logging.info('Enabled gyroscope on device.')
            return True

    def rate(self, deg: bool = False) -> tuple:
        """
            Returns gyroscope rotation rate in radians per second [rad/s], if gyroscope
            is unavailable returns empty tuple.
            @param deg: Should method convert returning value to degrees per second [deg/s]? 
        """
        try:
            x, y, z = gyroscope.rotation
            if deg:
                x = degrees(x)
                y = degrees(y)
                z = degrees(z)
            return (x, y, z)
        except Exception as e:
            logging.error('Error occured when tried to read gyroscope sensor data: %s', e)
            return self.NO_GYRO_VALUE

