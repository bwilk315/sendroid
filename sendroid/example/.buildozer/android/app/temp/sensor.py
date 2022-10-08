
from kivy.utils     import platform
from importlib      import import_module

class Sensor:
    """
        Class used to describe the behavior most sensors follow.
    """
    NO_ERROR        = 0
    ACCESS_ERROR    = 1
    READ_ERROR      = 2

    def __init__(self, ignore_platform: bool = False, req_perms: list = []):
        """
            Initializes the 'Sensor' class instance.
            @param ignore_platform: Should platform checking be omitted?
            @param req_perms:       List of android permissions required for sensor to work properly.
        """
        self.active             = False
        self.ignore_platform    = ignore_platform
        self.error              = Sensor.NO_ERROR
        self.req_perms          = [f'android.permission.{perm}' for perm in req_perms]
        # If platform ignorance is true, omit the rest (platform validation).
        if self.ignore_platform:
            return
        # Validate device's platform, and continue work if it is android.
        assert platform == 'android', 'Sorry, Sendroid supports only android devices.'
        self.mod_perms = import_module('android.permissions')  # Import android.permissions module for future management.

    def __enter__(self):
        """
            Method called when this context manager gets instantiated.
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
            Method called when context manager (this) gets destructed.
        """
        self._on_disable()

    def set_active(self, is_active: bool):
        """
            Either enables (if disabled) or disables (if enabled) the sensor.
            User is asked for required permissions if they were not granted already.
            @param is_active:   Should sensor be activated?
        """
        # If platform is ignored, next lines of code after this statement makes no sense, return early.
        if self.ignore_platform:
            return
        # Perform proper action which depends on the current state of sensor.
        if is_active and not self.active:
            # Find permissions which are not already granted by the user.
            needed_perms = [perm for perm in self.req_perms if not self.mod_perms.check_permission(perm)]
            # Request for needed permissions from user device, sensor activity boolean is set later by callback.
            if len(needed_perms):
                self.mod_perms.request_permissions(needed_perms, self.__on_perm_prompts_close)
            else:
                self.__on_perm_prompts_close([], [])
        elif not is_active and self.active:
            self._on_disable()
            self.active = False

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        """
            Callback invoked when user closes all permission prompts.
            @params permissions:    List of permissions user has been asked for.
            @params grants:         List of boolean values indicating which permissions from the list did user grant respectively.
            @returns:               Whether sensor is able to work without permission errors.
        """
        raise NotImplementedError()

    def _on_enable(self):
        """
            Method called when current sensor is enabled and all permission prompts are closed.     
        """
        raise NotImplementedError()

    def _on_disable(self):
        """
            Method called when current sensor is disabled.
        """
        raise NotImplementedError()

    def __on_perm_prompts_close(self, permissions, grants):
        """
            Callback invoked when all permission prompt windows are closed.
            This callback is like pipe - it is used only to set activity of the sensor which
            depends on another method result.
        """
        if self._on_perms_grant(permissions, grants):
            self.active = True
            self._on_enable()

