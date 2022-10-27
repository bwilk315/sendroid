

from kivy.utils     import platform

# Check if platform is supported.
if platform is not 'android':
    raise Exception('Your system is not supported by Bridge.')

# Import modules.
from importlib      import import_module    # Module used to import permissions module from p4a module.
from typing         import Dict, List       # Typings are useful especially in this project.
from ._java_stuff   import JSensor, sensorManager

class Manager():
    def __init__(self):
        # Import module for managing permissions.
        self.mod_perms      = import_module('android.permissions')
        # Get basic elements of an application (Activity, Context).
        
        self.__req_callback = lambda grants: None  # Callback used for storing user-defined behaviour on perms

    def has_perms(self, names: List[str]) -> Dict[str, bool]:
        """
            Returns the dictionary of permissions needed to check as keys and their grant state as boolean value
            (if a perm is granted value is True otherwise False).
        """
        result = {}
        # Check each permission included in list.
        for name in names:
            result[name] = self.mod_perms.check_permission(f'android.permission.{name}')
        return result

    def req_perms(self, names: List[str], callback = lambda grants: None):
        """
            Requests every permission included in the list and calls the user-defined behaviour
            with dictionary full of key (permission) value (grant state) pairs.
            @param names:       List of permission names to request.
            @param callback:    Behaviour called on request finish with results as a dictionary.
        """
        self.__req_callback = callback  # Save user-defined callback function.
        # Prepend permission names with their package and request for them.
        self.mod_perms.request_permissions([f'android.permission.{name}' for name in names], self.__on_req_finish)

    @property
    def device_sensors(self) -> List[str]:
        """
            Returns the list of supported sensors on the current device.
        """
        # Firstly get all sensors supported (in java type is denoted as List<Sensor>).
        java_sensors    = sensorManager.getSensorList(JSensor.TYPE_ALL)
        # Convert java list to python list.
        py_sensors      = [java_sensors[i] for i in range(java_sensors.size())]
        # Return the names of sensors using fast for loop.
        return [sensor.getName() for sensor in py_sensors]

    def __on_req_finish(self, perms: List[str], grants: List[str]):
        """
            Callback used to catch request finish in order to rapidly convert data received
            into dictionary of permission-state pairs.
        """
        result = {}
        # Fill dictionary with key (permission name) value (grant state) pairs.
        for pair in enumerate(perms):
            result[pair[1]] = grants[pair[0]]
        # Call previously user-defined callback with the dictionary.
        self.__req_callback(result)
