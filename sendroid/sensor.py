

class Sensor:
    """
        Class used to describe the behavior most sensors follow.
    """

    def __init__(self):
        """
            Initializes the 'Sensor' class instance.
        """
        self.active = False  # Is the sensor activated?

    def __enter__(self):
        """
            Method called when this context manager gets instantiated.
        """
        self._on_enable()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
            Method called when context manager (this) gets destructed.
        """
        self._on_disable()

    def set_active(self, is_active: bool):
        """
            Either enables (if disabled) or disables (if enabled) the sensor.
            @param is_active:   Should sensor be activated?
        """
        if is_active and not self.active:
            self._on_enable()
        elif not is_active and self.active:
            self._on_disable()
        self.active = is_active

    def _on_enable(self):
        """
            Method called when current sensor is enabled.
        """
        raise NotImplementedError

    def _on_disable(self):
        """
            Method called when current sensor is disabled.
        """
        raise NotImplementedError

