
from    plyer   import bluetooth as bt
from    .sensor import Sensor


class Bluetooth(Sensor):
    STATE_UNKNOWN   = 0
    STATE_OFF       = 1
    STATE_ON        = 2

    def __init__(self, **kwargs):
        super().__init__(
            # buildozer.spec: No requirements.
            req_perms = [],
            **kwargs
        )

    @property
    def state(self) -> str:
        """
            Returns the current state of bluetooth sensor (on or off).
        """
        info = bt.info
        return Bluetooth.STATE_OFF if info == 'off' else (Bluetooth.STATE_ON if info == 'on' else Bluetooth.STATE_UNKNOWN)

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        return True

    def _on_disable(self):
        self.on_disable()

    def _on_enable(self):
        self.on_enable()

