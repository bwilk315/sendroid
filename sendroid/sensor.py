
from kivy.utils     import platform

# Check if platform is supported.
if platform is not 'android':
    raise Exception('Only android devices are supported by Sendroid.')

# Classes used for making extending java classes and implementing java interfaces possible.
from jnius          import PythonJavaClass
# Decorator used to mark method as the one belonging to the class or interface extended.
from jnius          import java_method

from typing         import List

from ._java_stuff   import JSensor, JSensorEvent, JSensorManager, sensorManager


class Sensor(PythonJavaClass):
    # This static variable tells which interfaces are implemented by the class.
    __javainterfaces__  = ['android/hardware/SensorEventListener']
    JSensor             = JSensor
    JSensorManager      = JSensorManager

    def __init__(self, type: int, delay: int = JSensorManager.SENSOR_DELAY_NORMAL):
        """
            Initializes the 'Sensor' class instance.
            @param type:    Type of a sensor to listen.
            @param delay:   Type of delaying the sensor data readings.
        """
        self.type       = type
        self.delay      = delay
        self.values     = []
        self.accuracy   = JSensorManager.SENSOR_STATUS_NO_CONTACT
        self.sensor     = sensorManager.getDefaultSensor(type)

    def __del__(self):
        self.disable()

    @java_method('(Landroid/hardware/Sensor;I)V')
    def onAccuracyChanged(self, sensor: JSensor, accuracy: int):
        self.accuracy = accuracy  # Catch new accuracy.

    @java_method('(Landroid/hardware/SensorEvent;)V')
    def onSensorChanged(self, event: JSensorEvent):
        self.values = event.values  # Catch sensor values list.

    @staticmethod
    def get_list() -> List[str]:
        """
            Returns the list of supported sensors on the current device.
        """
        # Firstly get all sensors supported (in java type is denoted as List<Sensor>).
        java_sensors    = sensorManager.getSensorList(JSensor.TYPE_ALL)
        # Convert java list to python list.
        py_sensors      = [java_sensors[i] for i in range(java_sensors.size())]
        # Return the names of sensors using fast for loop.
        return [str(sensor.getName()).lower() for sensor in py_sensors]

    def enable(self):
        """
            Enable the sensor, this registers it as a new listener.
        """
        # Java parameters: (listener, sensor, samplingPeriodUs)
        sensorManager.registerListener(self, self.sensor, self.delay)

    def disable(self):
        """
            Disable the sensor listener registered ealier.
        """
        # Java parameters: (listener)
        sensorManager.unregisterListener(self)

