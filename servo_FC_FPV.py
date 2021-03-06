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
vehicle = connect(connectionString, wait_ready=["groundspeed","attitude","location.global_relative_frame"], baud=57600)

# Set USB capture device, set time stamp, codec, and video recorder
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_FFMPEG,True)
cap.set(cv2.CAP_PROP_FPS,30)

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

# Targetting calcs
def targeting(groundSpeed, altitude, roll, pitch):
    scale = 5

    dropTime = math.sqrt((2.0*altitude)/9.81)
    distance = int(dropTime * groundSpeed)
    xCorrection = int((math.tan(roll)) * altitude * scale)                  # Positive y is up
    yCorrection = int((distance - math.tan(pitch) * altitude) * scale)      # Positive x is right

    return (dropTime, distance, xCorrection, yCorrection, scale)

# Set all servos to closed
vehicle.channels.overrides['6'] = 2000
vehicle.channels.overrides['7'] = 2000
vehicle.channels.overrides['8'] = 2000

# Vehicle must be armed for throttle to work
while not vehicle.armed:
    print("Waiting for arming...")
    print(vehicle.armed)
    time.sleep(1)

# Display message
print("Open video feed")

# Main Loop
while(True):
    # Capture frame-by-frame, resize, and convert to grey then back to color so we can display color markers
    ret, frame = cap.read()
    frame = cv2.resize(frame, (width,height))
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    color = cv2.cvtColor(grey, cv2.COLOR_GRAY2BGR)

    # Get real time info from plane and process it
    (groundSpeed, roll, pitch, altitude) = getFlightData()
    (dropTime, distance, xCorrection, yCorrection, scale) = targeting(groundSpeed, altitude, roll, pitch)
    altitude = int(altitude*3.28084)

    # Print data to screen
    cv2.putText(color,"Current Altitude (ft): %s"%altitude,(1000,40),font,fontScale1,fontColor,lineType)
    cv2.putText(color,"Ground speed (m/s): %s"%round(groundSpeed,2),(1000,60),font,fontScale1,fontColor,lineType)
    cv2.putText(color,"X correction (m): %s"%round(xCorrection/scale,2),(1000,80),font,fontScale1,fontColor,lineType)
    cv2.putText(color,"Y correction (m): %s"%round(yCorrection/scale,2),(1000,100),font,fontScale1,fontColor,lineType)

    now = datetime.datetime.now()
    timeStamp = now.strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(color,timeStamp,(1000,20),font,fontScale1,fontColor,lineType)

    # Cross Hair
    crossHairColor = (0,255,0)
    cv2.line(color,(width/2+10+xCorrection,height/2+10-yCorrection),(width/2+30+xCorrection,height/2+30-yCorrection),crossHairColor,5)
    cv2.line(color,(width/2-10+xCorrection,height/2+10-yCorrection),(width/2-30+xCorrection,height/2+30-yCorrection),crossHairColor,5)
    cv2.line(color,(width/2+10+xCorrection,height/2-10-yCorrection),(width/2+30+xCorrection,height/2-30-yCorrection),crossHairColor,5)
    cv2.line(color,(width/2-10+xCorrection,height/2-10-yCorrection),(width/2-30+xCorrection,height/2-30-yCorrection),crossHairColor,5)

    cv2.circle(color, (width/2+xCorrection,height/2-yCorrection),5,crossHairColor,-1)

    # Display the linear altitude
    altVisual(color, altitude)

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

    # Display the resulting frame
    cv2.imshow("Aero HLG DAS - servo_FC_FPV.py",color)

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()

# Close the vehicle connection
vehicle.close()

print("Closing video feed")
