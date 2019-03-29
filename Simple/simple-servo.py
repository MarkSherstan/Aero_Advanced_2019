import cv2
import random
import math
import datetime
import time
import numpy as np
from dronekit import connect, VehicleMode, Command, LocationGlobal
from pymavlink import mavutil

# Text formatting
font        = cv2.FONT_HERSHEY_SIMPLEX
fontScale1  = 0.6
fontScale2  = 5.5
fontColor   = (0,255,0)
lineType    = 2

# Variable definition(s)
width = 1280
height = 720
record = False

CDA = False
WATER = False
HABITAT = False

# Connect to vehicle
connectionString = "/dev/tty.usbserial-DN04T9FH"
print "Connecting on: ",connectionString
vehicle = connect(connectionString, wait_ready=["location.global_relative_frame"], baud=57600)

# Set background, set time stamp, codec, and video recorder
color = np.zeros((height,width,3), np.uint8)

now = datetime.datetime.now()
timeStamp = now.strftime("%Y-%m-%d_%H.%M.%S") + ".avi"

out = cv2.VideoWriter(timeStamp,cv2.VideoWriter_fourcc('M','J','P','G'), 15, (width,height))

# Get telemetry data
def getFlightData():
    altitude = vehicle.location.global_relative_frame.alt
    if altitude < 0:    # Dont let the dropTime become imaginary
        altitude = 0

    return altitude

# Set all servos to closed
vehicle.channels.overrides['1'] = 1000
vehicle.channels.overrides['2'] = 2000
vehicle.channels.overrides['3'] = 1000
vehicle.channels.overrides['4'] = 2000
vehicle.channels.overrides['6'] = 2000

# Display message
print("Starting")

# Main Loop
while(True):
    # Create a black background
    color = np.zeros((height,width,3), np.uint8)

    # Get real time info from plane and process it
    altitude = getFlightData()
    altitude = int(altitude*3.28084)

    # Print data to screen
    cv2.putText(color,"Current Altitude (ft): %s"%altitude,(1030,40),font,fontScale1,fontColor,lineType)

    now = datetime.datetime.now()
    timeStamp = now.strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(color,timeStamp,(1030,20),font,fontScale1,fontColor,lineType)

    # Keyboard Toggles
    key = cv2.waitKey(1)

    if key != -1:
        if key == ord('1'):
            CDA = True
            droppedCDA = str(altitude)
            cv2.putText(color,"CDA",(10,150),font,fontScale2,(255,255,255),lineType)
            cv2.putText(color,droppedCDA+" ft",(10,300),font,fontScale2,(255,255,255),lineType)
            cv2.imwrite('CDA_Release.png',color)

            vehicle.channels.overrides['6'] = 1000
            vehicle.flush()

        elif key == ord('2'):
            HABITAT = True
            droppedHabitat = str(altitude)
            cv2.putText(color,"Habitat",(10,height-200),font,fontScale2,(255,255,255),lineType)
            cv2.putText(color,droppedHabitat+" ft",(10,height-50),font,fontScale2,(255,255,255),lineType)
            cv2.imwrite('habitat_Release.png',color)

            vehicle.channels.overrides['1'] = 2000
            vehicle.channels.overrides['2'] = 1000
            vehicle.flush()

        elif key == ord('3'):
            WATER = True
            droppedWater = str(altitude)
            cv2.putText(color,"Water",(750,height-200),font,fontScale2,(255,255,255),lineType)
            cv2.putText(color,droppedWater+" ft",(750,height-50),font,fontScale2,(255,255,255),lineType)
            cv2.imwrite('water_Release.png',color)

            vehicle.channels.overrides['3'] = 2000
            vehicle.channels.overrides['4'] = 1000
            vehicle.flush()

        elif key == ord('r'):
            if record == False:
                record = True
            else:
                record = False

        elif key == ord('q'):
            break

    if CDA == True:
        cv2.putText(color,"CDA",(10,150),font,fontScale2,(255,255,255),lineType)
        cv2.putText(color,droppedCDA+" ft",(10,300),font,fontScale2,(255,255,255),lineType)
        vehicle.channels.overrides['6'] = 1000
        vehicle.flush()
    else:
        vehicle.channels.overrides['6'] = 2000
        vehicle.flush()

    if HABITAT == True:
        cv2.putText(color,"Habitat",(10,height-200),font,fontScale2,(255,255,255),lineType)
        cv2.putText(color,droppedHabitat+" ft",(10,height-50),font,fontScale2,(255,255,255),lineType)
        vehicle.channels.overrides['1'] = 2000
        vehicle.channels.overrides['2'] = 1000
        vehicle.flush()
    else:
        vehicle.channels.overrides['1'] = 1000
        vehicle.channels.overrides['2'] = 2000
        vehicle.flush()

    if WATER == True:
        cv2.putText(color,"Water",(750,height-200),font,fontScale2,(255,255,255),lineType)
        cv2.putText(color,droppedWater+" ft",(750,height-50),font,fontScale2,(255,255,255),lineType)
        vehicle.channels.overrides['3'] = 2000
        vehicle.channels.overrides['4'] = 1000
        vehicle.flush()
    else:
        vehicle.channels.overrides['3'] = 1000
        vehicle.channels.overrides['4'] = 2000
        vehicle.flush()

    # Record footage and display red or white circle
    if record == True:
        cv2.circle(color, (20,height-20),5,(0,0,255),-1)
        out.write(color)
    else:
        cv2.circle(color, (20,height-20),5,(255,255,255),-1)

    # Display the resulting frame
    cv2.imshow("Aero HLG DAS - servo.py",color)

# When everything done, release the capture
out.release()
cv2.destroyAllWindows()

# Close the vehicle connection
vehicle.close()

print("Closing")
