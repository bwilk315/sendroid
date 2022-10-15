
from plyer import barometer as bar
from .sensor import Sensor


class Barometer(Sensor):
    NO_DATA = 0

    def __init__(self, **kwargs):
        super().__init__(
            # buildozer.spec: No requirements.
            req_perms = [],
            **kwargs
        )

    @property
    def pressure(self):
        """
            Returns the ambient air pressure in hecto pascals [hPa].
        """
        pres = bar.pressure
        return Barometer.NO_DATA if pres is None else pres

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        return True

    def _on_disable(self):
        bar.disable()
        self.on_disable()

    def _on_enable(self):
        bar.enable()
        self.on_enable()
