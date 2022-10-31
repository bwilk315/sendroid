# Sendroid
### Description
The project has been created in purpose of making android devices useful in inventing field, it supports sensors that are supported by device.\
It does fantastic work when fused with the [cliserc](https://pypi.org/project/cliserc/) module (my another one) which manages a simple client-server communication in Python 3.\
Every example presented in this documentation shows only how to use the project, you have to embed this knowledge in your Kivy application.
### Structure
Main package called _sendroid_ contains single module _sensor_ which defines the _Sensor_ class used to create sensor readers.
##### Checking supported sensors
Use _get_list_ static method of _Sensor_ class to get list of all sensors supported by the current device:
```python
from sendroid.sensor import Sensor

# Show all supported sensor names in readable format.
print('Supported sensors:\n', '\n'.join(Sensor.get_list()))
```
##### Reading sensor data
To read sensor (here accelerometer) data first check if it is supported using _get_list_ static method which returns list of strings (sensor names). Note that names are always in lower case and may vary on other devices, for you I suggest printing the list first and finding the name of what you really need:
```python
from sendroid.sensor import Sensor

supp = Sensor.get_list()
# Check if accelerometer sensor is supported.
if 'accelerometer' in supp:
    ...
```
Then if check succeed, create an instance of _Sensor_ class which will target accelerometer sensor:
```python
acc = Sensor(
    Sensor.JSensor.TYPE_ACCELEROMETER,  # Type of sensor.
    Sensor.JSensorManager.SENSOR_DELAY_NORMAL  # Type of delaying read operations.
    )
```
All possible sensor types are described [there](https://developer.android.com/reference/android/hardware/Sensor#TYPE_ACCELEROMETER) and types of delays [there](https://developer.android.com/reference/android/hardware/SensorManager#SENSOR_DELAY_FASTEST). _JSensor_ and _JSensorManager_ subclasses are java classes which contain constant values used above (reference to links). Enable the sensor using _enable_ method. You should disable it with _disable_ method when you are done:
```python
acc.enable()
```
Sensor data is stored in member list called _values_ and sensor accuracy level in _accuracy_ member variable. _values_ length depends on the sensor type for example here we want to read accelerometer sensor data; we know that it should return three values: _x_, _y_ and _z_ (the total acceleration) so _values_ list will contain three elements which are these axes:
```python
while True:
    # Show acceleration on three axes.
    print('Accelerometer data: {} {} {}'.format(*acc.values))
    print(f'Accuracy level: {acc.accuracy}')

acc.disable()  # Disable the sensor!
```
For more information about amount of items in _values_ list per specific type of sensor read [this](https://developer.android.com/reference/android/hardware/SensorEvent#values), about possible accuracy levels [this](https://developer.android.com/reference/android/hardware/SensorManager#SENSOR_STATUS_ACCURACY_HIGH).