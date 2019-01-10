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
connectionString = 'com8'
print "Connecting on: ",connectionString
vehicle = connect(connectionString, wait_ready=["groundspeed","attitude","location.global_relative_frame"], baud=57600)

# Set background, set time stamp, codec, and video recorder
color = np.zeros((height,width,3), np.uint8)

now = datetime.datetime.now()
timeStamp = now.strftime("%Y-%m-%d_%H.%M.%S") + ".avi"

out = cv2.VideoWriter(timeStamp,cv2.VideoWriter_fourcc('M','J','P','G'), 15, (width,height))

# Displays the altitude on right side od screen as a linear representation
def altVisual(color, altitude):
    drawColor = (0,255,0)
    locationX = 1150
    upperY = 200
    lowerY = 700
    alt50 = upperY + 333 #upperY + (lowerY-upperY)*((150.0-50)/150.0)
    alt100 = upperY + 167 #upperY + (lowerY-upperY)*((150.0-100)/150.0)

    currentAlt = int(upperY + (lowerY-upperY)*((150.0-altitude)/150.0))

    cv2.line(color,(locationX-25,currentAlt+25),(locationX,currentAlt),drawColor,2)
    cv2.line(color,(locationX-25,currentAlt-25),(locationX,currentAlt),drawColor,2)
    cv2.putText(color,str(altitude),(locationX-60,currentAlt+5),font,0.75,drawColor,2)

    cv2.putText(color,"Alt",(locationX,upperY-25),font,0.75,drawColor,2)    # Title
    cv2.line(color,(locationX,lowerY),(locationX,upperY),drawColor,1)       # Vertical Line

    cv2.line(color,(locationX,lowerY),(locationX+25,lowerY),drawColor,2)    # Bottom Line
    cv2.line(color,(locationX,upperY),(locationX+25,upperY),drawColor,2)    # Top Line
    cv2.line(color,(locationX,alt50),(locationX+25,alt50),drawColor,2)      # 50 ft
    cv2.line(color,(locationX,alt100),(locationX+25,alt100),drawColor,2)    # 100 ft

    cv2.putText(color,"0 ft",(locationX+30,lowerY),font,0.5,drawColor,2)
    cv2.putText(color,"50 ft",(locationX+30,alt50),font,0.5,drawColor,2)
    cv2.putText(color,"100 ft",(locationX+30,alt100),font,0.5,drawColor,2)
    cv2.putText(color,"150 ft",(locationX+30,upperY),font,0.5,drawColor,2)

# Get telemetry data [ m/s, radians, radians, m ]
def getFlightData():
    groundSpeed = vehicle.groundspeed
    roll = vehicle.attitude.roll
    pitch = vehicle.attitude.pitch
    altitude = vehicle.location.global_relative_frame.alt
    if altitude < 0:    # Dont let the dropTime become imaginary
        altitude = 0

    return (groundSpeed, roll, pitch, altitude)

# Set all servos to closed
vehicle.channels.overrides['6'] = 2000
vehicle.channels.overrides['7'] = 2000
vehicle.channels.overrides['8'] = 2000

# Display message
print("Starting")

# Main Loop
while(True):
    # Create a black background
    color = np.zeros((height,width,3), np.uint8)

    # Get real time info from plane and process it
    (groundSpeed, roll, pitch, altitude) = getFlightData()
    altitude = int(altitude*3.28084)

    # Print data to screen
    cv2.putText(color,"Current Altitude (ft): %s"%altitude,(1000,40),font,fontScale1,fontColor,lineType)
    cv2.putText(color,"Ground speed (m/s): %s"%round(groundSpeed,2),(1000,60),font,fontScale1,fontColor,lineType)
    cv2.putText(color,"Roll (deg): %s"%round(math.degrees(roll),2),(1000,80),font,fontScale1,fontColor,lineType)
    cv2.putText(color,"Pitch (deg): %s"%round(math.degrees(pitch),2),(1000,100),font,fontScale1,fontColor,lineType)

    now = datetime.datetime.now()
    timeStamp = now.strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(color,timeStamp,(1000,20),font,fontScale1,fontColor,lineType)

    # Keyboard Toggles
    key = cv2.waitKey(1)

    if key != -1:
        if key == ord('1'):
            CDA = True
            droppedCDA = str(altitude)
            cv2.putText(color,"CDA",(10,150),font,fontScale2,(255,255,255),lineType)
            cv2.putText(color,droppedCDA+" ft",(10,300),font,fontScale2,(255,255,255),lineType)
            cv2.imwrite('CDA_Release.png',color)

            vehicle.channels.overrides['5'] = 1000
            vehicle.flush()

        elif key == ord('2'):
            HABITAT = True
            droppedHabitat = str(altitude)
            cv2.putText(color,"Habitat",(10,height-200),font,fontScale2,(255,255,255),lineType)
            cv2.putText(color,droppedHabitat+" ft",(10,height-50),font,fontScale2,(255,255,255),lineType)
            cv2.imwrite('habitat_Release.png',color)

            vehicle.channels.overrides['6'] = 1000
            vehicle.flush()

        elif key == ord('3'):
            WATER = True
            droppedWater = str(altitude)
            cv2.putText(color,"Water",(750,height-200),font,fontScale2,(255,255,255),lineType)
            cv2.putText(color,droppedWater+" ft",(750,height-50),font,fontScale2,(255,255,255),lineType)
            cv2.imwrite('water_Release.png',color)

            vehicle.channels.overrides['7'] = 1000
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
        vehicle.channels.overrides['7'] = 1000
        vehicle.flush()
    else:
        vehicle.channels.overrides['7'] = 2000
        vehicle.flush()

    if WATER == True:
        cv2.putText(color,"Water",(750,height-200),font,fontScale2,(255,255,255),lineType)
        cv2.putText(color,droppedWater+" ft",(750,height-50),font,fontScale2,(255,255,255),lineType)
        vehicle.channels.overrides['8'] = 1000
        vehicle.flush()
    else:
        vehicle.channels.overrides['8'] = 2000
        vehicle.flush()

    # Record footage and display red or white circle
    if record == True:
        cv2.circle(color, (20,height-20),5,(0,0,255),-1)
        out.write(color)
    else:
        cv2.circle(color, (20,height-20),5,(255,255,255),-1)

    # Display the linear altitude
    altVisual(color, altitude)

    # Display the resulting frame
    cv2.imshow("Aero HLG DAS - servo.py",color)

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()

# Close the vehicle connection
vehicle.close()

print("Closing")
