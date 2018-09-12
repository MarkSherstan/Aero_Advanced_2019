# Aero_HLG_Targeting_II
V2 Targeting and DAS system for Advanced Class SAE Aero Design competition. Python and OpenCV upgrade from previous Java/Processing program located [here](https://github.com/MarkSherstan/Aero_HLG_2018_DAS).

## To be completed...
* Activate servo (possible hardware / wiring connection issue)

## Usage
Change line 21 to your serial port / USB Port in a format similar to:
* Linux - /dev/ttyUSB0
* OSX - dev/cu.usbmodem1
* Windows - com14

You can look up the value in Arduino IDE --> Tools --> Port. Using a Mac my line 21 looks like:

```
connectionString = "/dev/tty.usbserial-DN02WF3K"
```

The following are case sensative:
* r --> Toggle recording (will rewrite file if it is turned on off on).
* (space) --> Release payload.
* q --> Exit program, must be used to ensure recording is properly saved.

## Requirments
Built using:
* [Python](https://www.python.org) 2.7.15
* [OpenCV](https://opencv.org) 3.4.2
* [Dronekit](http://python.dronekit.io) 2.9.1
* [pySerial](https://pypi.org/project/pyserial/) 3.4

## Help
Before first connection connect with [QGroundControl](http://qgroundcontrol.com) to ensure communication and help limit time out delays. 

## Hardware
* Pixhawk px4 Flight Controller
* 915 MHz SiK Telemetry Radio
* Servo to be connected to port 6?
