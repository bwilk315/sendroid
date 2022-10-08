
from    plyer   import bluetooth
from    .sensor import Sensor
import  logging


class Bluetooth(Sensor):
    """
        Management class for bluetooth sensor.
    """

    def __init__(self) -> None:
        super().__init__()

    def on_disable(self) -> None:
        pass

    def on_enable(self) -> bool:
        error = len(bluetooth.info) == 0
        if error: 
            logging.error('Success: bluetooth sensor is accessible.')
        else:
            logging.info('Bluetooth sensor is inaccesible')
        return error

    @property
    def info(self) -> str:
        """
            Returns the info received from bluetooth sensor.
        """
        return bluetooth.info

