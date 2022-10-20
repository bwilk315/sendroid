
from .sensor    import Sensor
from plyer      import humidity as hum


class Humidity(Sensor):
    NO_DATA = .0

    def __init__(self, **kwargs):
        super().__init__(
            # buildozer.spec: No requirements.
            req_perms = [],
            **kwargs
        )

    @property
    def value(self) -> float:
        """
            Returns humidity in percents [%] if it is available, otherwise returns 0.
        """
        try:
            return hum.tell
        except:
            return Humidity.NO_DATA

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        return True

    def _on_enable(self):
        hum.enable()
        self.on_enable()

    def _on_disable(self):
        hum.disable()
        self.on_disable()

