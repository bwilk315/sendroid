
"""
    File contains 'Sensor' class, it should be used to instantiate new sensor manager; you choose
    the type of sensor from supported ones (class constants), and a way of delaying the sensor
    job (also class constants). Sensor data is stored in dynamic list 'values' which contains
    appropriate amount of data for specific sensor.
"""

# Classes used for making extending java classes and implementing java interfaces possible.
from jnius          import PythonJavaClass
# Decorator used to mark method as the one belonging to the class or interface extended.
from jnius          import java_method
# Import some java stuff.
from ._java_stuff   import JSensor, JSensorEvent, JSensorManager, sensorManager


class Sensor(PythonJavaClass):
    # This static variable tells which interfaces are implemented by the class.
    __javainterfaces__  = ['android/hardware/SensorEventListener']

    # Types of supported sensors.
    TYPE_ACCELEROMETER                  = JSensor.TYPE_ACCELEROMETER  # [X]
    TYPE_MAGNETIC_FIELD                 = JSensor.TYPE_MAGNETIC_FIELD  # [X]
    TYPE_ORIENTATION                    = JSensor.TYPE_ORIENTATION  # [X]
    TYPE_GYROSCOPE                      = JSensor.TYPE_GYROSCOPE  # [X]
    TYPE_LIGHT                          = JSensor.TYPE_LIGHT  # [X]
    TYPE_PROXIMITY                      = JSensor.TYPE_PROXIMITY  # [X]
    TYPE_GRAVITY                        = JSensor.TYPE_GRAVITY  # [X]
    TYPE_LINEAR_ACCELERATION            = JSensor.TYPE_LINEAR_ACCELERATION  # [X]
    TYPE_ROTATION_VECTOR                = JSensor.TYPE_ROTATION_VECTOR  # [X]
    TYPE_MAGNETIC_FIELD_UNCALIBRATED    = JSensor.TYPE_MAGNETIC_FIELD_UNCALIBRATED  # [X]
    TYPE_GAME_ROTATION_VECTOR           = JSensor.TYPE_GAME_ROTATION_VECTOR  # [X]
    # TYPE_SIGNIFICANT_MOTION           = JSensor.TYPE_SIGNIFICANT_MOTION
    # TYPE_STEP_DETECTOR                  = JSensor.TYPE_STEP_DETECTOR
    TYPE_STEP_COUNTER                   = JSensor.TYPE_STEP_COUNTER  # [X]
    TYPE_GEOMAGNETIC_ROTATION_VECTOR    = JSensor.TYPE_GEOMAGNETIC_ROTATION_VECTOR  # [X]
    # TYPE_TILT_DETECTOR                = JSensor.TYPE_TILT_DETECTOR
    # TYPE_WAKE_GESTURE                 = JSensor.TYPE_WAKE_GESTURE
    # TYPE_GLANCE_GESTURE               = JSensor.TYPE_GLANCE_GESTURE
    # TYPE_PICK_UP                      = JSensor.TYPE_PICK_UP
    # TYPE_DEVICE_ORIENTATION           = JSensor.TYPE_DEVICE_ORIENTATION
    # TYPE_STATIONARY_DETECT              = JSensor.TYPE_STATIONARY_DETECT
    # TYPE_MOTION_DETECT                = JSensor.TYPE_MOTION_DETECT
    # TYPE_STEP_DETECTOR_WAKEUP         = JSensor.TYPE_STEP_DETECTOR_WAKEUP

    # Delay types of a sensor readings.
    DELAY_FASTEST       = JSensorManager.SENSOR_DELAY_FASTEST
    DELAY_GAME          = JSensorManager.SENSOR_DELAY_GAME
    DELAY_NORMAL        = JSensorManager.SENSOR_DELAY_NORMAL
    DELAY_UI            = JSensorManager.SENSOR_DELAY_UI

    def __init__(self, type: int, delay: int = DELAY_NORMAL):
        """
            Initializes the 'Sensor' class instance.
            @param type:    Type of a sensor to listen.
            @param delay:   Type of delaying the sensor data readings.
        """
        self.type       = type
        self.delay      = delay
        self.accuracy   = 0
        self.values     = []
        self.sensor     = sensorManager.getDefaultSensor(type)

    def __del__(self):
        self.disable()

    @java_method('(Landroid/hardware/Sensor;I)V')
    def onAccuracyChanged(self, sensor: JSensor, accuracy: int):
        self.accuracy = accuracy  # Catch new accuracy.

    @java_method('(Landroid/hardware/SensorEvent;)V')
    def onSensorChanged(self, event: JSensorEvent):
        self.values = event.values  # Catch sensor values list.

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

