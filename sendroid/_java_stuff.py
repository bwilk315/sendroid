
"""
    This python file contains java classes' location constants, followed with the actual
    java classes got using these constant values, they are prefixed with capital 'j' letter
    to show that they are stolen from java language.
    Class instances are defined then, they are especially useful. 
"""

from jnius import autoclass, cast

# Java class packages.
CLS_PYTHON_ACTIVITY         = 'org.kivy.android.PythonActivity'
CLS_ACTIVITY                = 'android.app.Activity'
CLS_CONTEXT                 = 'android.content.Context'
CLS_SENSOR_MANAGER          = 'android.hardware.SensorManager'
CLS_SENSOR                  = 'android.hardware.Sensor'
CLS_SENSOR_EVENT            = 'android.hardware.SensorEvent'
CLS_SENSOR_EVENT_LISTENER   = 'android.hardware.SensorEventListener'
CLS_LIST                    = 'java.util.List'

# Actual java classes.
JActivity                   = autoclass(CLS_ACTIVITY)
JContext                    = autoclass(CLS_CONTEXT)
JSensorManager              = autoclass(CLS_SENSOR_MANAGER)
JSensor                     = autoclass(CLS_SENSOR)
JSensorEvent                = autoclass(CLS_SENSOR_EVENT)
JSensorEventListener        = autoclass(CLS_SENSOR_EVENT_LISTENER)
JList                       = autoclass(CLS_LIST)

# Useful class instances.
activity        = cast(CLS_ACTIVITY,        autoclass(CLS_PYTHON_ACTIVITY).mActivity)
context         = cast(CLS_CONTEXT,         activity.getApplicationContext())
sensorManager   = cast(CLS_SENSOR_MANAGER,  context.getSystemService(JContext.SENSOR_SERVICE))
