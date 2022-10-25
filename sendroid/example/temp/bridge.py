
from kivy.utils     import platform

# Check if platform is supported.
if platform is not 'android':
    raise Exception('Your system is not supported by Bridge.')

# Import modules.
from importlib      import import_module    # Module used to import permissions module from p4a module.
from typing         import Dict, List       # Typings are useful especially in this project.
from jnius          import cast, autoclass  # Import neccessary functions to interact with java classes.

# Java class packages.
CLS_PYTHON_ACTIVITY         = 'org.kivy.android.PythonActivity'
CLS_ACTIVITY                = 'android.app.Activity'
CLS_CONTEXT                 = 'android.content.Context'
CLS_SENSOR_MANAGER          = 'android.hardware.SensorManager'
CLS_SENSOR                  = 'android.hardware.Sensor'
CLS_SENSOR_EVENT            = 'android.hardware.SensorEvent'
CLS_SENSOR_EVENT_LISTENER   = 'android.hardware.SensorEventListener'
CLS_LIST                    = 'java.util.List'

# Actual java class references.
JActivity                   = autoclass(CLS_ACTIVITY)
JContext                    = autoclass(CLS_CONTEXT)
JSensorManager              = autoclass(CLS_SENSOR_MANAGER)
JSensor                     = autoclass(CLS_SENSOR)
JSensorEvent                = autoclass(CLS_SENSOR_EVENT)
JSensorEventListener        = autoclass(CLS_SENSOR_EVENT_LISTENER)
JList                       = autoclass(CLS_LIST)

# -------------------- BRIDGE LOGIC --------------------

class Bridge():
    def __init__(self):
        # Import module for managing permissions.
        self.mod_perms              = import_module('android.permissions')
        # Get basic elements of an application (Activity, Context).
        self.activity               = cast(CLS_ACTIVITY,         autoclass(CLS_PYTHON_ACTIVITY).mActivity)
        self.context                = cast(CLS_CONTEXT,          self.activity.getApplicationContext())
        self.sensor_mgr             = cast(CLS_SENSOR_MANAGER,   self.context.getSystemService(JContext.SENSOR_SERVICE))
        self.__req_callback         = lambda grants: None  # Callback used for storing user-defined behaviour on perms

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

    def get_sensor(self, type: int) -> JSensor:
        """
            Returns the reference to sensor with specified type.
            @param type:    Type of sensor (use Bridge.JSensor.TYPE_<SensorName> constant).
        """
        return self.sensor_mgr.getDefaultSensor(type)

    @property
    def device_sensors(self) -> List[str]:
        """
            Returns the list of supported sensors on the current device.
        """
        # Firstly get all sensors supported (in java type is denoted as List<Sensor>).
        java_sensors    = self.sensor_mgr.getSensorList(JSensor.TYPE_ALL)
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


# -------------------- SENSORS --------------------

"""
********** JNI-COMPATIBLE SIGNATURE GUIDE **********
    L<java class>; = represent a Java object of the type <java class>
    Z = represent a java/lang/Boolean;
    B = represent a java/lang/Byte;
    C = represent a java/lang/Character;
    S = represent a java/lang/Short;
    I = represent a java/lang/Integer;
    J = represent a java/lang/Long;
    F = represent a java/lang/Float;
    D = represent a java/lang/Double;
    V = represent void, available only for the return type
    All the types can have the [ prefix to design an array. The return type can be V or empty.
"""

# Import essentials to work strictly with java.
from jnius import PythonJavaClass   # Class used for making extending java classes and implementing java interfaces possible.
from jnius import java_method       # Decorator used to mark method as the one belonging to the class or interface extended.

class Sensor(PythonJavaClass):
    # This static variable tells which interfaces are implemented by the class.
    __javainterfaces__  = ['android/hardware/SensorEventListener']

    def __init__(self, type: int, delay: int):
        """
            Initializes the 'Sensor' class instance.
            @param type:    Type of a sensor to listen (Use pattern: JSensor.TYPE_<SensorName>).
            @param delay:   Delay in miliseconds [ms] which is applied to the.
        """
        self.type   = type
        self.delay  = delay
        self.bridge = Bridge()
        self.sensor = self.bridge.get_sensor(type)
        self.data   = []

    @java_method('(Landroid/hardware/Sensor;I)V')
    def onAccuracyChanged(self, sensor: JSensor, accuracy: int):
        # Do something here if sensor accuracy changes.
        ...

    @java_method('(Landroid/hardware/SensorEvent;)V')
    def onSensorChanged(self, event: JSensorEvent):
        self.data = event.values  # Catch sensor values list.

    def start(self):
        # Register sensor listener (this class).
        self.bridge.sensor_mgr.registerListener(self, self.sensor, self.delay)

    def stop(self):
        # Stop the listener by unregistering it.
        self.bridge.sensor_mgr.unregisterListener(self)

