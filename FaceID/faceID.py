import cv2
import os
import sys
import io
import time
import getpass
from datetime import datetime
import requests as req
import json
import numpy as np
from PIL import Image
from django.core.files import File
from gpiozero import MotionSensor

# Add web app directory to path so its constants can be referenced
sys.path.append(os.path.join(os.environ["GGPATH"], "GGProject"))
from GreeterGuru import settings
# Import function used for handling unrecognized faces
from handleUnrecognizedFaces import validateEmployee
# Import functions used for managing the photo dataset
import managePhotoDataset as mpd


# Trains images in the dataset
def trainDataset():

    photoRegister = mpd.readPhotoNames()

    if len(photoRegister) > 0:

        path = 'dataset'
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")

        def getImagesAndLabels(path):

            imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
            faceSamples = []
            ids = []

            for imagePath in imagePaths:

                picName = os.path.split(imagePath)[-1]
                ext = picName.split(".")[1]

                if ext == "jpg":
                    id = int(picName.split("_")[0])
                    PIL_img = Image.open(imagePath).convert('L')
                    img_numpy = np.array(PIL_img,'uint8')

                    faces = detector.detectMultiScale(img_numpy)
                    for (x,y,w,h) in faces:
                        faceSamples.append(img_numpy[y:y+h,x:x+w])
                        ids.append(id)
            return faceSamples,ids

        faces,ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))
        recognizer.write('trainer/trainer.yml')


# checks if employee's face data exists
def employeeExist(empID, photoRegister):

    for person in photoRegister:
        extractEmpID = person[1].split("_")[0]
        if (int(extractEmpID) == empID):
            return(True)
        else:
            return(False)


# Initializes a new employee
def initializeEmployee(empID, url, headers, cam):

    photoRegister = mpd.readPhotoNames()
    photoNum = 0
    person = [':']
    frameCount = 20

    while(True):

        # Get camera feed
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        detector = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")
        faces = detector.detectMultiScale(gray, 1.3, 5)

        # Add given number of detected faces to database/photoRegister
        for (x,y,w,h) in faces:

            photoNum += 1

            # Add photo to photoRegister
            newPhotoName = str(empID) + '_' + str(photoNum) + ".jpg"
            person.append(newPhotoName.strip(".jpg"))

            # Convert captured frame to bytes/file object
            image = Image.fromarray(gray[y:y+h,x:x+w])
            imageFile = io.BytesIO()
            image.save(imageFile, "JPEG")
            imageFile.seek(0)

            # Post the picture to the proper Employee in the database
            imageFile.name = newPhotoName
            files = {"file" : imageFile}
            response = req.post(url + "pictures/" + str(empID) + "/", headers=headers, files=files)

        # Exit after adding given number of pictures
        # or by manually exiting with wait key (esc)
        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27 or photoNum >= frameCount:
            break

    # Disconnect camera
    cam.release()
    cv2.destroyAllWindows()

    # Update photoRegister, text file, last scan, and re-train
    photoRegister.append(person)
    mpd.writePhotoNames(photoRegister)
    mpd.recordLastScan(int(empID))
    trainDataset()


# Detects and identifies registered employee faces
def detectFace(url, headers):

    photoRegister = mpd.readPhotoNames()

    if len(photoRegister) == 0:
        pass

    # Facial recognition and detection tools
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "cascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Initialize camera
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # Widht
    cam.set(4, 480) # Height
    # Face size threshold
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    # Initialize variables
    count = 0
    accuracyList = []
    avgAccuracy = -1
    accThreshold = 25
    lock = True
    camWait = 10 # camera timeout limit in seconds
    timeStamp = time.time()


    # Within camera timeout limit
    while (np.abs(int((time.time() - timeStamp))) < camWait):

        # Get current image
        ret, img = cam.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Face detection tools
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )

        # Detect faces
        for(x,y,w,h) in faces:

            timeStamp = time.time()

            # Recognize faces
            EmpID, accuracy = recognizer.predict(gray[y:y+h,x:x+w])

            # Compute accuracy average
            accuracy = round(100 - accuracy)
            if 0 < accuracy <= 100:
                if (count < 10):
                    accuracyList.append(accuracy)
                    avgAccuracy = -1
                    count += 1
                elif (count >= 10):
                    avgAccuracy = np.average(accuracyList)
                    accuracyList = [accuracy] + accuracyList
                    accuracyList.pop()
            else:
                count = 0
                accuracyList = []
                avgAccuracy = -1

            # Accuracy passes threshold
            if (avgAccuracy > accThreshold):

                # Run once when unlocked
                if lock == True:
                    lock = False

                for person in photoRegister:
                    extractEmpID = person[1].split("_")[0]

                    if (int(extractEmpID) == EmpID):

                        # Get employee's last scan date and today's date
                        lastScan = person[0]
                        currentDate = datetime.now().strftime("%Y:%m:%d")

                        # If employee hasn't entered in the past day
                        if lastScan != currentDate:

                            # Update employee's photos
                            for i in range(5):

                                # Shift photo names
                                photoName = mpd.registerShift(EmpID, 5)
                                response = req.delete(url + "pictures/" + photoName + "/") # delete current photo

                                # Convert captured frame to bytes/file object
                                image = Image.fromarray(gray[y:y+h,x:x+w])
                                imageFile = io.BytesIO()
                                image.save(imageFile, "JPEG")
                                imageFile.seek(0)

                                # Post the picture to the proper Employee in the database
                                imageFile.name = photoName  + ".jpg"
                                files = {"file" : imageFile}
                                if photoName != "none":
                                    response = req.post(url + "pictures/" + str(EmpID) + "/", files=files, headers=headers) # add newly captured photo

                            # Log last face scan time
                            mpd.recordLastScan(EmpID)


            # Accuracy does not pass threshold
            elif (avgAccuracy <= 10) and (avgAccuracy > 0):

                # Run once when locked
                if lock == False:
                    lock = True

                employee = validateEmployee(url, headers)

                if employee != -1:
                    empExist = employeeExist(employee, photoRegister)
                    if not empExist:
                        initializeEmployee(employee, url, headers, cam)
                    else:
                        # Update employee's photos
                        for i in range(10):

                            # Shift photo names
                            photoName = mpd.registerShift(employee, 10)
                            response = req.delete(url + "pictures/" + photoName + "/") # delete current photo

                            # Convert captured frame to bytes/file object
                            image = Image.fromarray(gray[y:y+h,x:x+w])
                            imageFile = io.BytesIO()
                            image.save(imageFile, "JPEG")
                            imageFile.seek(0)

                            # Post the picture to the proper Employee in the database
                            imageFile.name = photoName  + ".jpg"
                            files = {"file" : imageFile}
                            if photoName != "none":
                                response = req.post(url + "pictures/" + str(employee) + "/", files=files, headers=headers) # add newly captured photo

                        # Log last face scan time
                        mpd.recordLastScan(employee)

        # Press 'ESC' for exiting video
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

    # Stop camera feed
    cam.release()
    cv2.destroyAllWindows()
    return()


# Continuously checks PIR sensor for motion
def senseMotion(pir, url, headers):

    # Halt program until motion is detected, then detect faces
    while True:
        pir.wait_for_motion()
        detectFace(url, headers)


# Will be replaced with proximity sensor control loop
def main():

    # Stores photo names for each person as a 2D list
    photoRegister = []

    # Website's API url
    url = settings.WEB_URL + "api/"

    # Retrieve website's admin's credentials for authentication
    username = settings.WEB_USERNAME
    password = getpass.getpass("Web admin's password: ")
    data = {"username": username, "password": password}

    # Create authorization header for authenticating HTTP requests
    response = req.post(url + "token-auth/", json = data)
    token = response.json()["token"]
    headers = {"Authorization" : "Token " + token}

    # Load PIR motion sensor
    pir = MotionSensor(4)

    senseMotion(pir, url, headers)
