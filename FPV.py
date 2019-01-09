import cv2

# Required to communicate with USB capture device
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_FFMPEG,True)
cam.set(cv2.CAP_PROP_FPS,30)

# Get frame, resize, and display forever until someone enters q
while(True):
    ret,frame = cam.read()
    frameNew = cv2.resize(frame, (1920,1080))
    cv2.imshow('FPV Video Feed',frameNew)

    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

# Clear connections and window
cam.release()
cv2.destroyAllWindows()
