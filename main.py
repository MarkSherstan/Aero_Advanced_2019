import cv2
import random
import math
import datetime
import numpy as np
from dronekit import connect, VehicleMode, Command, LocationGlobal
from pymavlink import mavutil

# Text formatting
font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 0.6
fontColor              = (0,255,0)
lineType               = 2

# Variable definition(s)
width = 1280
height = 720
dropped = False
record = False

# Connect to vehicle
connectionString = "/dev/tty.usbserial-DN02WF3K"
print "Connecting on: ",connectionString
vehicle = connect(connectionString, wait_ready = ["groundspeed","attitude","location.global_relative_frame"], baud = 57600)

# Camera properties, set time stamp, codec, and video recorder
cap = cv2.VideoCapture(0)
ret = cap.set(3,width)
ret = cap.set(4,height)

now = datetime.datetime.now()
timeStamp = now.strftime("%Y-%m-%d_%H.%M.%S") + ".avi"

out = cv2.VideoWriter(timeStamp,cv2.VideoWriter_fourcc('M','J','P','G'), 15, (width,height))

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

# Drop Servo
def activateServo(PWM):
    msg = vehicle.message_factory.command_long_encode(
    0, 0,                                       # target_system, target_component
    mavutil.mavlink.MAV_CMD_DO_SET_SERVO,       # command
    0,                                          # confirmation
    9,                                          # servo number
    PWM,                                        # servo position between 1000 and 2000
    0, 0, 0, 0, 0)                              # param 3-7 not used

    vehicle.send_mavlink(msg)

print("Open video feed")

# Main Loop
while(True):
    # Capture frame-by-frame, convert to grey then back to color so we can display color markers
    ret, frame = cap.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    color = cv2.cvtColor(grey, cv2.COLOR_GRAY2BGR)

    # Get real time info from plane and process it
    (groundSpeed, roll, pitch, altitude) = getFlightData()
    (dropTime, distance, xCorrection, yCorrection, scale) = targeting(groundSpeed, altitude, roll, pitch)

    # Print data to screen
    cv2.putText(color,"Altitude (m): %s"%round(altitude,2),(10,20),font,fontScale,fontColor,lineType)
    cv2.putText(color,"Ground speed (m/s): %s"%round(groundSpeed,2),(10,40),font,fontScale,fontColor,lineType)
    cv2.putText(color,"X correction (m): %s"%round(xCorrection/scale,2),(10,60),font,fontScale,fontColor,lineType)
    cv2.putText(color,"Y correction (m): %s"%round(yCorrection/scale,2),(10,80),font,fontScale,fontColor,lineType)

    if dropped == False:
        cv2.putText(color,"payload armed",(width/2 - 50,height-20),font,fontScale,(255,255,255),lineType)
    else:
        cv2.putText(color,"payload released",(width/2 - 60,height-20),font,fontScale,(255,255,255),lineType)

    # Cross Hair
    if altitude < 30.5:
        crossHairColor = (255,0,255) # Magenta
    else:
        crossHairColor = (0,255,0)

    cv2.line(color,(width/2+10+xCorrection,height/2+10-yCorrection),(width/2+30+xCorrection,height/2+30-yCorrection),crossHairColor,5)
    cv2.line(color,(width/2-10+xCorrection,height/2+10-yCorrection),(width/2-30+xCorrection,height/2+30-yCorrection),crossHairColor,5)
    cv2.line(color,(width/2+10+xCorrection,height/2-10-yCorrection),(width/2+30+xCorrection,height/2-30-yCorrection),crossHairColor,5)
    cv2.line(color,(width/2-10+xCorrection,height/2-10-yCorrection),(width/2-30+xCorrection,height/2-30-yCorrection),crossHairColor,5)

    cv2.circle(color, (width/2+xCorrection,height/2-yCorrection),5,crossHairColor,-1)

    # Record footage and display red or white circle
    if record == True:
        cv2.circle(color, (20,height-20),5,(0,0,255),-1)
        out.write(color)
    else:
        cv2.circle(color, (20,height-20),5,(255,255,255),-1)

    # Display the resulting frame
    cv2.imshow("Aero DAS and Vision System",color)

    # Keyboard Toggles
    key = cv2.waitKey(1)

    if key != -1:
        if key == ord(' '):
            dropped = True
            cv2.rectangle(color, (width/2 - 150, height), (width/2 + 150, height-60), (0,0,0), -1)
            cv2.putText(color,"payload released",(width/2 - 80,height-20),font,fontScale,(255,255,255),lineType)
            cv2.imwrite('payload_Release.png',color)
            activateServo(1000)
        elif key == ord('r'):
            if record == False:
                record = True
            else:
                record = False
        elif key == ord('q'):
            break

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()

# Close the vehicle and/or simulator
vehicle.close()
