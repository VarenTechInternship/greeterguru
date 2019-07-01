import numpy as np
import cv2


faceCascade = cv2.CascadeClassifier('/home/gg/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
#faceCascade = cv2.CascadeClassifier("/home/pi/opencv-3.3.0/data/haarcascades/home/pi/opencv-3.3.0/data/haarcascades")
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height


while True:

    ret, img = cap.read()
    #	img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (20, 20)
    )

    for (x,y,w,h) in faces:
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.circle(img, int((x+(w/2)), int(y-(h/2))), int(h/2), (0, 255, 0), 1, 8, 0)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
    cv2.imshow('video', img)
    k = cv2.waitKey(30) & 0xff

    if k == 27: # press 'ESC' to quit
        break

cap.release()
cv2.destroyAllWindows()
