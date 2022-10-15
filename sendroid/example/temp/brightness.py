
from plyer      import brightness       as brig
from jnius      import autoclass, cast
from .sensor    import Sensor


class Brightness(Sensor):
    def __init__(self, **kwargs):
        super().__init__(
            # buildozer.spec: WRITE_SETTINGS.
            req_perms = [],
            **kwargs
        )

    @property
    def level(self):
        return brig.current_level()

    @level.setter
    def level(self, value: int):
        # Clamp the value in proper range.
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        # Set brightness level.
        brig.set_level(value)

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        return True

    def _on_disable(self):
        self.on_disable()

    def _on_enable(self):
        self.on_enable()

