
from    plyer       import battery  as bat
from    .sensor     import Sensor


class Battery(Sensor):
    def __init__(self, **kwargs) -> None:
        """
            Initializes the 'Accelerometer' class instance.
            @kwarg ignore_platform:     Should platform checking be omitted?
            @kwarg on_error[int, str]:  Error callback, called with the error information.
        """
        self.on_error   = kwargs.get('on_error',    lambda code, info: None)
        self.on_enable  = kwargs.get('on_enable',   lambda: None)
        self.on_disable = kwargs.get('on_disable',  lambda: None)
        super().__init__(
            ignore_platform=kwargs.get('ignore_platform', False),
            # buildozer.spec: BATTERY_STATS.
            req_perms=[]
        )

    @property
    def charging(self) -> bool:
        """
            Returns whether device battery is in charging state. False is returned
            when data is not accessible.
        """
        return bat.status['isCharging']

    @property
    def percent(self) -> float:
        """
            Returns the percent of battery filling if data is accessible, otherwise
            0 is returned.
        """
        perc = bat.status['percentage']
        return .0 if perc is None else perc

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        print('>><<>><<>>', permissions, " > ", grants)
        return all(grants)

    def _on_disable(self):
        self.on_disable()

    def _on_enable(self):
        self.on_enable()

