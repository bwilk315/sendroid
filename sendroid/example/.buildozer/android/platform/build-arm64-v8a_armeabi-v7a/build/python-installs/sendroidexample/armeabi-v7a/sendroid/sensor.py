
class Sensor:
    """
        Class used to describe the behavior most sensors follow.
    """
    def __init__(self, **kwargs) -> None:
        """
            Initializes the 'Sensor' class instance.
        """
        pass

    def __enter__(self) -> None:
        self.on_enable()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.on_disable()

    def start(self):
        """
            Starts the current sensor job.
        """
        self.__enter__()

    def close(self):
        """
            Finishes the sensor job started earlier.
        """
        self.__exit__(None, None, None)

    def on_enable(self) -> None:
        """
            Method called when sensor gets enabled (started).
        """
        pass

    def on_disable(self) -> None:
        """
            Method called if current sensor has been disabled (closed).
        """
        pass
