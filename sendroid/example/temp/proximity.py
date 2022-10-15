
from plyer      import proximity
from .sensor    import Sensor


class Proximity(Sensor):
    def __init__(self, **kwargs):
        super().__init__(
            # buildozer.spec: No requirements.
            req_perms = [],
            **kwargs
        )

    @property
    def covered(self) -> bool:
        if self.active:
            return proximity.proximity
        else:
            self.on_error(Sensor.READ_ERROR, 'Proximity sensor is not accessible.')
            return False

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        return True

    def _on_disable(self):
        proximity.disable()
        self.on_disable()

    def _on_enable(self):
        try:
            proximity.enable()
        except:
            self.on_error(Sensor.ACCESS_ERROR, 'Can not enale the proximity sensor device.')
        else:
            self.on_enable()
