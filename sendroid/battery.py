
from    plyer   import battery
from    .sensor import Sensor
import  logging


class Battery(Sensor):
    """
        Management class for battery sensor.
    """

    def __init__(self) -> None:
        super().__init__()

    def on_disable(self) -> None:
        pass

    def on_enable(self) -> bool:
        error = battery.get_state() is None
        if error:
            logging.error('Failed to enable the battery sensor on device: %s', e)
        else:
            logging.info('Enabled battery sensor on device.')
        return error

    @property
    def is_charging(self) -> bool:
        """
            Returns whether device's battery is in charging mode.
        """
        return battery.status['isCharging']
    
    @property
    def test(self) -> float:
        return battery.get_state()

    @property
    def percentage(self) -> float:
        """
            Returns the fraction of battery fill level.
        """
        return battery.status['percentage']
