
"""
    List of sendroid module examples, build them (separately!) and find out the use of all supported sensors :).
    To build an example simply uncomment the import statement and method call then build application, with buildozer
    you can build with command: "buildozer android debug deploy run".

    Bartłomiej Wilk (c) 2022
"""

def extra_example():
    """
        Runs the data sender example.
    """
    from cliserc.simplex    import Simplex
    from bnot               import BNot
    from temp.gyroscope     import Gyroscope
    from time               import sleep

    def on_send(resp: BNot, dt: float) -> BNot:
        sleep(.01)  # Apply send interval.
        # Get rotation of device in space.
        rot                         = gyro.rotation
        return BNot(data            = {
            'response': Simplex.RES_OK,
            'rx':       rot[0],
            'ry':       rot[1],
            'rz':       rot[2]
        })

    # Create instance of connection manager.
    client          = Simplex(
        '192.168.0.200',
        6000,
        is_server   = False,
        on_send     = on_send,
    )
    # Create gyroscope sensor manager, and activate it.
    gyro            = Gyroscope(
        mode        = Gyroscope.DEG_MODE
    )
    gyro.set_active(True)
    # Start client and connect to a server.
    client.start()
    client.connect(create_thread = True)

# extra_example()

# ********** PROTOTYPING **********

import    ex_prototype

ex_prototype.     run_prototype()

# ********** SENDROID EXAMPLES **********
# import    ex_accelerometer
# import    ex_audio
# import    ex_battery
# import    ex_brightness
# import    ex_gyroscope
# import    ex_light
# import    ex_vibrator

# ex_accelerometer. run_example()
# ex_audio.         run_example()
# ex_battery.       run_example()
# ex_brightness.    run_example()
# ex_gyroscope.     run_example()
# ex_light.         run_example()
# ex_vibrator.      run_example()

