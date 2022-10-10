
from plyer      import light
from .sensor    import Sensor


class Light(Sensor):
    # Class specific.
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
            Returns the value of light sensor in luxes [lx].
        """
        illum = light.illumination
        return Light.NO_DATA if illum is None else illum
    
    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        return True

    def _on_disable(self):
        light.disable()
        self.on_disable()

    def _on_enable(self):
        light.enable()
        self.on_enable()

