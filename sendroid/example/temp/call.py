
from .sensor    import Sensor
from plyer      import call


class Call(Sensor):
    def __init__(self, **kwargs):
        super().__init__(
            # buildozer.spec: CALL_PHONE.
            req_perms = [
                'CALL_PHONE'
            ],
            **kwargs
        )

    def make(self, tel: int):
        """
            Makes a call to the specified number.
            @param tel: Phone number with country prefix e.g. +48.
        """
        if self.active:
            call.makecall(tel)
        else:
            #! Program was unable to access the call sensor.
            self.on_error(Sensor.ACCESS_ERROR)
    
    def dial(self):
        """
            Opens the dialling interface for inputting the phone number.
        """
        if self.active:
            call.dialcall()
        else:
            #! Program was unable to access the call sensor.
            self.on_error(Sensor.ACCESS_ERROR)
        
    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        return all(grants)

    def _on_enable(self):
        self.on_enable()

    def _on_disable(self):
        self.on_disable()

