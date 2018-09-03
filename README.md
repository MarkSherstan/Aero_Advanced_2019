# Aero_HLG_Targeting_II
V2 Targeting and DAS system for Advanced Class SAE Aero Design competition. Python and OpenCV upgrade from previous Processing/Java program located [here](https://github.com/MarkSherstan/Aero_HLG_2018_DAS).

## To be completed...
* Complete tests in place of simulator

## Usage
Run file as follows:
```
python main.py --connect (USB Port)
```
Where (USB Port) follows a format similar to:
* Linux - /dev/ttyUSB0
* OSX - dev/cu.usbmodem1
* Windows - com14

The following are case sensative:
* r --> Toggle recording (will rewrite file if it is turned on off on).
* (space) --> Release payload.
* q --> Exit program, must be used to ensure recording is properly saved.

## Requirments
Built using:
* [Python](https://www.python.org) 2.7.15
* [OpenCV](https://opencv.org) 3.4.2
* [Dronekit](http://python.dronekit.io) 2.9.1

## Hardware
* Pixhawk px4 Flight Controller
* 915 MHz SiK Telemetry Radio
* Servo to be connected to port 6
