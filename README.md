# Aero_Advanced_2019
2019 Data Acquisition System (DAS) for UofA's Aero HLG Advanced Class aircraft for the SAE Aero Design competition. Upgraded from 2018's program located [here](https://github.com/MarkSherstan/Aero_HLG_Targeting_II).

## To be completed
Transition from channel overrides to DO_SET_SERVO.

```
msg = vehicle.message_factory.command_long_encode(
0, 0,                                 # target_system, target_component
mavutil.mavlink.MAV_CMD_DO_SET_SERVO, # command
0,                                    # confirmation
1,                                    # servo number
1500,                                 # servo position between 1000 and 2000
0, 0, 0, 0, 0)                        # param 3 ~ 7 not used

vehicle.send_mavlink(msg)
```

## Usage
Change line 26 to your serial port / USB Port in a format similar to:
* Linux - /dev/ttyUSB0
* OSX - dev/tty.usbserial
* Windows - com14

You can look up the value in Arduino IDE --> Tools --> Port. Using a Mac my line 22 looks like:

```
connectionString = "/dev/tty.usbserial-DN04K54A"
```

The following are case sensative:
* r --> Toggle recording (will write file with current time stamp).
* 1 --> Release CDA.
* 2 --> Release habitat.
* 3 --> Release water.
* q --> Exit program, must be used to ensure recording is properly saved.

## Requirements
Built using:
* [Python](https://www.python.org) 2.7.15
* [OpenCV](https://opencv.org) 3.4.2
* [Dronekit](http://python.dronekit.io) 2.9.1
* [pySerial](https://pypi.org/project/pyserial/) 3.4

## Help
Before first connection, connect with [QGroundControl](http://qgroundcontrol.com) to ensure communication and help limit time out delays.

Ensure firmware is up to date on Telemetry Radios. Using QGroundControl go to, Vehicle set up --> Firmware --> and follow onscreen instructions.

The latests version of Ardupilot is required on the Pixhawk. Current PX4 software build does not support servo commands or channel overrides (September 2018).

## License
The MIT License (MIT)

## Hardware
* Pixhawk 4 Flight Controller
* 915 MHz SiK Telemetry Radio
* Dropping servos to be connected on channels 5, 6, and 7
