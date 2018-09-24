# Aero_HLG_Targeting_II
V2 Targeting and DAS system for Advanced Class SAE Aero Design competition. Python and OpenCV upgrade from previous Java/Processing program located [here](https://github.com/MarkSherstan/Aero_HLG_2018_DAS).

## Usage
Change line 22 to your serial port / USB Port in a format similar to:
* Linux - /dev/ttyUSB0
* OSX - dev/tty.usbserial
* Windows - com14

You can look up the value in Arduino IDE --> Tools --> Port. Using a Mac my line 22 looks like:

```
connectionString = "/dev/tty.usbserial-DN04K54A"
```

The following are case sensative:
* r --> Toggle recording (will write file with current time stamp).
* (space) --> Release payload.
* q --> Exit program, must be used to ensure recording is properly saved.

Crosshairs for targeting are purple unless altitude is greater than 100 ft (~30.5 m) AGL (crosshairs then turn green).

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
* Pixhawk px4 Flight Controller
* 915 MHz SiK Telemetry Radio
* Servo to be connected to channel 5 assigned pin
