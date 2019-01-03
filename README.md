# Aero_Advanced_2019
2019 Data Acquisition System (DAS) for UofA's Aero HLG Advanced Class aircraft for the SAE Aero Design competition. Upgraded from 2018's program located [here](https://github.com/MarkSherstan/Aero_HLG_Targeting_II).


## Usage
Change "connectionString" variable to serial port / USB Port in a format similar to:
* Linux - /dev/ttyUSB0
* OSX - dev/tty.usbserial
* Windows - com14

You can look up the value in Arduino IDE --> Tools --> Port. For example on my Mac the variable is set as:

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


## License
The MIT License (MIT)


## Hardware
* Pixhawk 4 Flight Controller
* 915 MHz SiK Telemetry Radio
* Dropping servos to be connected on channels 6, 7, and 8


## Help
Before first connection, connect with [QGroundControl](https://docs.qgroundcontrol.com/en/releases/daily_builds.html) (QGC) to ensure communication and help limit time out delays. The beta version or daily build must be used. Stable version will not work as of January 1, 2019.

Ensure firmware is up to date on Telemetry Radios. Using QGroundControl go to, Vehicle set up --> Firmware --> and follow onscreen instructions.

The latests version of Ardupilot is required on the Pixhawk. Current PX4 software build does not support servo commands or channel overrides (January 2019) ArduPlane 3.9.4 confirmed to be working and must be installed with ChibiOS.


## PX4 Parameters
AHRS_GPS_USE
ARMING_CHECK
SERVO_RC --> Write instructions 


## To do
* Bind the telemtry radios on specific channel
* Test with multiple servos
* OpenCV version and independent version
* Test [this](https://stackoverflow.com/questions/22146205/grab-frame-ntsctousb-dongle-opencv2-python-wrapper/22183737#22183737) fix for RCA connection


## Wiring and Connection Order
Receiver to PPM Encoder:
* Receiver = 1  |   PPM Encoder = 3
* Receiver = 2  |   PPM Encoder = 1
* Receiver = 3  |   PPM Encoder = 2
* Receiver = 4  |   PPM Encoder = 4
* Receiver = 5  |   PPM Encoder = 5   -->   SC Switch

I/O PWM Out:
* Channel 1 --> Pin 1 --> roll
* Channel 2 --> Pin 2 --> pitch
* Channel 3 --> Pin 3 --> Not working
* Channel 4 --> Pin 4 --> yaw
* Channel 5 --> Pin 5 --> Not working


## Other Notes
APM Planner 2.0.26-rc2_win64 (beta version - http://firmware.ardupilot.org/Tools/APMPlanner/beta/). Also works on stable version on mac OS.

Mission Planner 1.3.58 (beta version? - http://firmware.ardupilot.org/Tools/MissionPlanner/beta/) is required to flash new firmware (ArduPlane) due to FMUv5.

Builds for more development van be found [here](http://firmware.ardupilot.org/)
