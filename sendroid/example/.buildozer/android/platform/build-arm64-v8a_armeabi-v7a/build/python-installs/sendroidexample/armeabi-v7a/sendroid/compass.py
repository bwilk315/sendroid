
from    plyer      import compass
from    .sensor     import Sensor
import  logging


class Compass(Sensor):
    """
        Management class for compass sensor.
    """
    NO_COMPASS_VALUE = (.0, .0, .0)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def on_disable(self) -> None:
        compass.disable()

    def on_enable(self) -> None:
        try:
            compass.enable()
        except Exception as e:
            logging.error('Failed to enable the compass sensor on device: %s', e)
            return False
        else:
            logging.info('Enabled compass sensor on device.')
            return True

    def field(self) -> tuple:
        """
            Returns compass sensor value which is a magnetic field.
        """
        try:
            x, y, z = compass.field
            return (x, y, z)
        except Exception as e:
            logging.error('Error occured when tried to read compass sensor data: %s', e)
            return self.NO_COMPASS_VALUE

