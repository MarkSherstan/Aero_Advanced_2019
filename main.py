import numpy as np
import cv2
import random
import math

# Text
font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (200,200)
fontScale              = 0.5
fontColor              = (0,255,0)
lineType               = 2

# Variable definition(s)
width = 640
height = 480
dropped = False
record = False

# Camera properties, codec, and video recorder
cap = cv2.VideoCapture(0)
ret = cap.set(3,width)
ret = cap.set(4,height)
out = cv2.VideoWriter('out.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 15, (width,height))

# Targetting calcs
def targeting(airSpeed, altitude, gyroRoll, gyroPitch):
    scale = 5   # One meter is equal to x pixels

    dropTime = math.sqrt((2*altitude)/9.81)
    distance = dropTime * airSpeed
    xCorrection = int((math.cos(gyroRoll)) * scale)
    yCorrection = int((math.cos(gyroPitch) + distance) * scale)
    return (dropTime, distance, xCorrection, yCorrection)

while(True):
    # Capture frame-by-frame, convert to grey then back to color so we can display color markers
    ret, frame = cap.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    color = cv2.cvtColor(grey, cv2.COLOR_GRAY2BGR)

    # Randomized data for target calcs
    airSpeed = random.randint(12, 14)
    altitude = random.randint(30, 34)
    gyroRoll = random.randint(0, 12);
    gyroPitch = random.randint(0, 5);

    (dropTime, distance, xCorrection, yCorrection) = targeting(airSpeed, altitude, gyroRoll, gyroPitch)

    # Print data to screen
    cv2.putText(color,"Arduino voltage (V): null",(10,20),font,fontScale,fontColor,lineType)
    cv2.putText(color,"Altitude (m): %s"%round(altitude,2),(10,40),font,fontScale,fontColor,lineType)
    cv2.putText(color,"Air speed (m/s): %s"%round(airSpeed,2),(10,60),font,fontScale,fontColor,lineType)
    cv2.putText(color,"Drop distance (m): %s"%round(distance,2),(10,80),font,fontScale,fontColor,lineType)

    if dropped == False:
        cv2.putText(color,"payload armed",(width/2 - 50,height-20),font,fontScale,(255,255,255),lineType)
    else:
        cv2.putText(color,"payload released",(width/2 - 60,height-20),font,fontScale,(255,255,255),lineType)

    # Cross Hair
    crossHairColor = (255,0,255) #(150,250,50)

    cv2.line(color,(width/2+10+xCorrection,height/2+10-yCorrection),(width/2+30+xCorrection,height/2+30-yCorrection),crossHairColor,5)
    cv2.line(color,(width/2-10+xCorrection,height/2+10-yCorrection),(width/2-30+xCorrection,height/2+30-yCorrection),crossHairColor,5)
    cv2.line(color,(width/2+10+xCorrection,height/2-10-yCorrection),(width/2+30+xCorrection,height/2-30-yCorrection),crossHairColor,5)
    cv2.line(color,(width/2-10+xCorrection,height/2-10-yCorrection),(width/2-30+xCorrection,height/2-30-yCorrection),crossHairColor,5)

    cv2.circle(color, (width/2+xCorrection,height/2-yCorrection),5,crossHairColor,-1)

    # Record footage and display red or white circle
    if record == True:
        out.write(color)
        cv2.circle(color, (20,height-20),5,(0,0,255),-1)
    else:
        cv2.circle(color, (20,height-20),5,(255,255,255),-1)

    # Display the resulting frame
    cv2.imshow("Aero DAS and Vision System",color)

    # Keyboard Toggles
    key = cv2.waitKey(1)

    if key != -1:
        if key == ord(' '):
            dropped = True
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
