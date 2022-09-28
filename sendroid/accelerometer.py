
from    plyer  import accelerometer
from    .sensor import Sensor
import  logging


class Accelerometer(Sensor):
    """
        Management class for accelerometer sensor.
    """
    NO_ACC_VALUE = (.0, .0, .0)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def on_disable(self) -> None:
        accelerometer.disable()

    def on_enable(self) -> bool:
        try:
            accelerometer.enable()
        except Exception as e:
            logging.error('Failed to enable the accelerometer on device: %s', e)
            return False
        else:
            logging.info('Enabled accelerometer on device.')
            return True

    def value(self) -> tuple:
        """
            Returns the value of accelerometer sensor.
            The value returned consists of three values (x, y and z)
            which represent the current acceleration of device (gravity is included).
        """
        try:
            return accelerometer.acceleration
        except Exception as e:
            logging.error('Error occured when tried to read accelerometer sensor data: %s', e)
            return self.NO_ACC_VALUE

