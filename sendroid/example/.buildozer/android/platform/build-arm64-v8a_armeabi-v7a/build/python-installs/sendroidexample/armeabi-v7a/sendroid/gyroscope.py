
from    plyer      import gyroscope
from    math       import degrees
from    .sensor     import Sensor
import  logging


class Gyroscope(Sensor):
    """
        Management class for gyroscope sensor.
    """
    NO_GYRO_VALUE = (.0, .0, .0)

    def __init__(self) -> None:
        super().__init__()

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

    def rate(self, uncalib: bool = False, deg: bool = False) -> tuple:
        """
            Returns gyroscope rotation rate in radians per second [rad/s], if gyroscope
            is unavailable returns empty tuple (it is filled with zeroes).
            @param uncalib: Specifies whether uncalibrated value should be read.
            @param deg:     Should method convert returning value to degrees per second [deg/s]? 
        """
        try:
            x, y, z = gyroscope.rotation_uncalib if uncalib else gyroscope.rotation
            if deg:
                x = degrees(x)
                y = degrees(y)
                z = degrees(z)
            return (x, y, z)
        except Exception as e:
            logging.error('Error occured when tried to read gyroscope sensor data: %s', e)
            return self.NO_GYRO_VALUE

