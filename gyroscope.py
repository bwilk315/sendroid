
from plyer      import gyroscope
from time       import time
from math       import degrees
import logging


class Gyroscope:
    def __init__(self, **kwargs) -> None:
        """
            Initializes a 'Gyroscope' class instance.
            @kwarg show_log:    If enabled, helpful log messages will be displayed in standard output.
        """
        self.show_logs  = kwargs.get('show_logs', False)
        self.__lrt      = time()
        # Disable logging if needed.
        if not self.show_logs:
            logging.disable()
        # Try to turn gyroscope on.
        try:
            gyroscope.enable()
        except Exception as e:
            logging.error('Failed to enable the gyroscope on device: %s', e)
            self.available = False
            return False
        else:
            logging.info('Enabled gyroscope on device.')
            self.available = True
            return True
        
    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        gyroscope.disable()

    def rate(self, deg=False) -> tuple:
        """
            Returns gyroscope rotation rate in radians per second [rad/s], if gyroscope
            is unavailable returns empty tuple.
            @param deg: Should method convert returning value to degrees per second [deg/s]? 
        """
        x, y, z = None, None, None
        if self.available:
            x, y, z = gyroscope.rotation
            if deg:
                x = degrees(x)
                y = degrees(y)
                z = degrees(z)
        return (x, y, z)

    def change(self, deg=False) -> tuple:
        """
            Computes a change of rotation in radians/degrees using delta time based on time
            interval counted from last call of method to the current.
            @param deg: Should the return value be in degrees [deg]?
        """
        r = self.rate()
        dt = time() - self.__lrt
        x, y, z = r[0] * dt, r[1] * dt, r[2] * dt
        if deg:
            x = degrees(x)
            y = degrees(y)
            z = degrees(z)
        self.__lrt = time()
        return (x, y, z)

