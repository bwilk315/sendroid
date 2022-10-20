
from plyer      import temperature as tem
from .sensor    import Sensor


class Temperature(Sensor):
    # Class-specific
    NO_DATA = 0

    def __init__(self, **kwargs):
        super().__init__(
            # buildozer.spec: No requirements.
            req_perms = [],
            **kwargs
        )

    @property
    def value(self) -> float:
        """
            Returns the ambient temperature in Celsius degrees (*C).
        """
        temp = tem.temperature
        return Temperature.NO_DATA if temp is None else temp

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        return True

    def _on_disable(self):
        tem.disable()
        self.on_disable()

    def _on_enable(self):
        tem.enable()
        self.on_enable()
