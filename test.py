import cv2
import random
import math
import datetime
import numpy as np
from dronekit import connect, VehicleMode, Command, LocationGlobal
from pymavlink import mavutil

# Text formatting
font          = cv2.FONT_HERSHEY_SIMPLEX
fontScale1    = 0.6
fontScale2    = 5.5
fontColor     = (0,255,0)
lineType      = 2

# Variable definition(s)
width = 1280
height = 720
record = False

CDA = False
WATER = False
HABITAT = False

# Camera properties, set time stamp, codec, and video recorder
cap = cv2.VideoCapture(0)
ret = cap.set(3,width)
ret = cap.set(4,height)

now = datetime.datetime.now()
timeStamp = now.strftime("%Y-%m-%d_%H.%M.%S") + ".avi"

out = cv2.VideoWriter(timeStamp,cv2.VideoWriter_fourcc('M','J','P','G'), 15, (width,height))

# Targetting calcs
def targeting(groundSpeed, altitude, roll, pitch):
    scale = 5

    dropTime = math.sqrt((2.0*altitude)/9.81)
    distance = int(dropTime * groundSpeed)
    xCorrection = int((math.tan(roll)) * altitude * scale)                  # Positive y is up
    yCorrection = int((distance - math.tan(pitch) * altitude) * scale)      # Positive x is right

    return (dropTime, distance, xCorrection, yCorrection, scale)

print("Open video feed")

# Main Loop
while(True):
    # Capture frame-by-frame, convert to grey then back to color so we can display color markers
    ret, frame = cap.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    color = cv2.cvtColor(grey, cv2.COLOR_GRAY2BGR)

    # Get real time info from plane and process it
    groundSpeed = random.randint(12,14)
    roll = 0.3
    pitch = 0.1
    altitude = random.randint(30,32)
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

    # Keyboard Toggles
    key = cv2.waitKey(1)

    if key != -1:
        if key == ord('1'):
            CDA = True
            droppedCDA = str(altitude)
            cv2.putText(color,"CDA",(10,150),font,fontScale2,(255,255,255),lineType)
            cv2.putText(color,droppedCDA+" ft",(10,300),font,fontScale2,(255,255,255),lineType)
            cv2.imwrite('CDA_Release.png',color)

        elif key == ord('2'):
            HABITAT = True
            droppedHabitat = str(altitude)
            cv2.putText(color,"Habitat",(10,height-200),font,fontScale2,(255,255,255),lineType)
            cv2.putText(color,droppedHabitat+" ft",(10,height-50),font,fontScale2,(255,255,255),lineType)
            cv2.imwrite('habitat_Release.png',color)

        elif key == ord('3'):
            WATER = True
            droppedWater = str(altitude)
            cv2.putText(color,"Water",(750,height-200),font,fontScale2,(255,255,255),lineType)
            cv2.putText(color,droppedWater+" ft",(750,height-50),font,fontScale2,(255,255,255),lineType)
            cv2.imwrite('water_Release.png',color)

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

    if HABITAT == True:
        cv2.putText(color,"Habitat",(10,height-200),font,fontScale2,(255,255,255),lineType)
        cv2.putText(color,droppedHabitat+" ft",(10,height-50),font,fontScale2,(255,255,255),lineType)

    if WATER == True:
        cv2.putText(color,"Water",(750,height-200),font,fontScale2,(255,255,255),lineType)
        cv2.putText(color,droppedWater+" ft",(750,height-50),font,fontScale2,(255,255,255),lineType)

    # Record footage and display red or white circle
    if record == True:
        cv2.circle(color, (20,height-20),5,(0,0,255),-1)
        out.write(color)
    else:
        cv2.circle(color, (20,height-20),5,(255,255,255),-1)

    # Display the resulting frame
    cv2.imshow("Aero DAS and Vision System",color)

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()

print("Closing video feed")
