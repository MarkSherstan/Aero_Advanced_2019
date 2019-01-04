# Aero_Advanced_2019
2019 Data Acquisition System (DAS) for UofA's Aero HLG Advanced Class aircraft for the SAE Aero Design competition. Upgraded from previous program located [here](https://github.com/MarkSherstan/Aero_HLG_2018_DAS).


## To do
- [ ] Bind the telemtry radios on specific channel
- [ ] Test with multiple servos
- [ ] OpenCV version and independent version
- [ ] Test [this](https://stackoverflow.com/questions/22146205/grab-frame-ntsctousb-dongle-opencv2-python-wrapper/22183737#22183737) fix for RCA connection --> Works in test. Confirm in code
- [ ] Hough Line Transform


## Requirements
Built using:
* [Python](https://www.python.org) 2.7.15
* [OpenCV](https://opencv.org) 3.4.2
* [Dronekit](http://python.dronekit.io) 2.9.1
* [pySerial](https://pypi.org/project/pyserial/) 3.4
* [numpy](http://www.numpy.org/) 1.15.4

All dependencies should be installed with it, otherwise follow the errors and post an issue so I can update the instructions.


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


## License
The MIT License (MIT)


## Hardware
* Pixhawk 4 Flight Controller
* 915 MHz SiK Telemetry Radio



## Help
Before first connection, connect with [QGroundControl](https://docs.qgroundcontrol.com/en/releases/daily_builds.html) (QGC) to ensure communication and help limit time out delays. The beta version or daily build must be used. Stable version will not work as of January 1, 2019.

Ensure firmware is up to date on Telemetry Radios. Using QGroundControl go to, Vehicle set up --> Firmware --> and follow onscreen instructions.

The latest version of ArduPilot is required on the Pixhawk. Current PX4 software build does not support servo commands or channel overrides (January 2019) ArduPlane 3.9.4 confirmed to be working and must be installed with ChibiOS.


## Wiring and Connection Order
Dropping servos to be connected on channels 6, 7, and 8 but not mapped to transmitter

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


## PX4 Parameters
AHRS_GPS_USE
ARMING_CHECK
SERVO_RC --> Write instructions


## Configuring Auxiliary (dropping) Servo
* Connect to Q Ground Control
* Navigate to parameters and search for SERVO\#\_FUNCTION where the ( ) is the number of the servo and change the parameter from disabled to RCIN ( )
* Value must be either 6, 7, or 8 as 1-4 are used for standard controls and 5 is for switching flight modes. Channels higher than 8 are not supported and these must not be mapped to the transmitter.


## Pairing Telemtry Radios
Use Mission Planner or APM Planner 2.0 follow the guide [here](http://ardupilot.org/copter/docs/common-configuring-a-telemetry-radio-using-mission-planner.html) to pair the radios on a specific channel. The radios are currently configured on Net ID



## FPV and OpenCV

### Hardware 
* AKK FX3 5.8 GHz FPV transmitter
* Duo5800v4.1 FPV receiver
* VC500 image capture device

### Transmitter and Receiver Tables 

#### FPV Transmitter Menu Table

| Btn Press | Description  | Values...|     	    |     	    |      	    |      	    |      	    |      	    |      	    |
| ----------| ------------ | -------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- |
| 1x	      | Channel	     | 1	      | 2	        | 3	        | 4	        | 5	        | 6	        | 7	        | 8	        |
| 2x	      | Band	       | A	      | b	        | E	        | F	        | r         |           |           |           |
| 3x	      | Power Level  | 25  	    | 200  	    | 400  	    | 600  	    |      	    |      	    |      	    |      	    |

#### FPV Transmitter Frequency Table

| Channel     | 1         | 2        | 3        | 4        | 5        | 6        | 7        | 8        |           |
| ----------- | --------- | -------- | ---------| -------- | -------- | -------- | -------- | -------- | --------- |
| 1 (Band A)  | 5865	    | 5845	   | 5825	    | 5805	   | 5785	    | 5765	   | 5745	    | 5725	   | MHZ	     |
| 2 (Band B)  | 5733 	    | 5752	   | 5771	    | 5790	   | 5809	    | 5828	   | 5847	    | 5866	   | MHZ	     |
| 3 (Band E)  | 5705	    | 5685	   | 5665	    | 5645	   | 5885	    | 5905	   | 5925	    | 5945	   | MHZ	     |
| 4 (Band F)  | 5740	    | 5760	   | 5780	    | 5800	   | 5820	    | 5840	   | 5860	    | 5880	   | MHZ	     |
| 5 (Race)	  | 5658	    | 5695	   | 5732	    | 5769	   | 5806	    | 5843	   | 5880	    | 5917	   | MHZ	     |
|             |           |          |          |          |          |          |          |          |           |  
| Power Level | 25        | 200      | 400      | 600      |          |          |          |          | mW        |  

#### FPV Receiver Frequency Table

| Channel / Band    | 1         | 2        | 3        | 4        | 5        | 6        | 7        | 8        |           |
| ----------------- | --------- | -------- | ---------| -------- | -------- | -------- | -------- | -------- | --------- |
| 1                 | 5740	    | 5760	   | 5780	    | 5800	   | 5820	    | 5840	   | 5860	    | 5880	   | IRC/Fs	   |
| 2                 | 5658	    | 5695	   | 5732	    | 5769	   | 5806	    | 5843	   | 5880	    | 5917	   | Race	     |
| 3                 | 5705	    | 5685	   | 5665	    | 5645	   | 5885	    | 5905	   | 5925	    | 5945	   | Band E	   |
| 4                 | 5733 	    | 5752	   | 5771	    | 5790	   | 5809	    | 5828	   | 5847	    | 5866	   | Band B	   |
| 5                 | 5865	    | 5845	   | 5825	    | 5805	   | 5785	    | 5765	   | 5745	    | 5725	   | Band A    |

### Video Feed from FPV
Should be blue not black when disconnected. Black indicates driver error. Try reinstalling and restarting computer or try [this](https://www.youtube.com/watch?v=0F2FuWTExoY) fix.
