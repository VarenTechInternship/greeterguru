# !/usr/bin/python

"""
*Testing foundation for FaceID functions*

In order to test, make sure that:
1. Opencv is successfully installed
2. Run "source ~/.profile && workon cv" before running program
   --> this puts you in the virtual environment with all necessary tools
"""

import cv2
import os
import sys
import numpy as np
from PIL import Image
from datetime import datetime
import time

import requests as req
import io
import json, getpass
from django.core.files import File
# For testing the server is local
url = "http://localhost:8000/api/"

# GLOBAL VARIABLES
photoRegister = [] # Stores photo names for each person as a 2D list
frameCount = 20 # the amount of frames to take and maintain for an employee
updateFrameCount = 5 # amount of frames to capture and update to a recognized employee
dayLim = 1 # [HOURS, MINS, SECS] --> the amount of time for the system to wait until updating that employee's photos again

# loads face detection model
face_detector = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')


# Reads the contents of the photoNames.txt file
def readPhotoRegister():
    
    photoNames = open("photoNames.txt", "r")
    tempPhotoRegister = photoNames.readlines()

    for i in range(len(tempPhotoRegister)):
        person = tempPhotoRegister[i]
        person = person.strip().split(",")
        tempPhotoRegister[i] = person

    photoNames.close()

    return(tempPhotoRegister)
 

# Writes new content to the photoNames.txt file
def writePhotoRegister():                                                                              

    global photoRegister 
    photoNames = open("photoNames.txt", "w") 

    photoNames.truncate()

    copy = []	
    for person in photoRegister:
        line = ",".join(person)
        copy.append(line)
        photoNames.write(line+"\n")

    photoNames.close()


# records UTC time stamp for an employee
def recordLastScan(empID):

    global photoRegister
    photoRegister = readPhotoRegister()

    currentDate = datetime.utcnow().date()
    stamp = str(currentDate.year) + ":" + str(currentDate.month) + ":" + str(currentDate.day)

    for person in photoRegister:
        extractEmpID = (person[1].split("_"))[0]
        if int(extractEmpID) == int(empID):
            person[0] = stamp

    writePhotoRegister()


def token():

    # Enter the admin's password
    # (getpass is used so the password doesn't have to be hard-coded into the program)
    password = getpass.getpass(prompt = "Admin Password: ")
    # Create the admin data
    data = {
        "username": "Admin",
        "password": password,
    }
    
    # Call a post request at the extension 'token-auth/' and pass the admin data
    response = req.post(url + "token-auth/", json = data)
    # Convert the response to a readable format
    content = response.json()
    # Extract the token
    token = content["token"]

    # Create a header for the HTTP request containing the token
    headers = {"Authorization" : "Token " + token}
    # Call whatever request you need and pass the header
    response = req.get(url + "employees/", headers = headers)
    # (All of the following example requests exclude this parameter for simplicity)


# Registers a new employee
def createEmployee():

    # 1. get employee ID
    # 2. take frames 
    # 3. append person to photoRegister --> [employeeID] + [photo#]
    # 4. add to dataset/ folder & send to database

    global photoRegister 
    photoRegister = readPhotoRegister()

    global frameCount
    photoNum = 0

    # Manages input for new employee ID
    flag = False
    while flag == False:
        empID = input("Enter your EMPLOYEE ID:  ")
        if len(photoRegister) == 0: 
            flag = True
        for person in photoRegister:
            extractEmpID = (person[1].split("_"))[0]
            if extractEmpID == empID:
                print("Employee already exists")
            else: flag = True

    # CAMERA INITIALIZATION
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # width
    cam.set(4, 480) # height

    person = [':']
    while(True):
    
        # get camera feed in gray
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(gray, 1.3, 5) # detects face

        # only while face is detected
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            photoNum += 1

            newPhotoName = str(empID) + '_' + str(photoNum) + ".jpg" # names photo
            person.append(newPhotoName.strip(".jpg")) # for txt file

            # Convert captured frame to Image object
            image = Image.fromarray(gray[y:y+h,x:x+w])
            # Create bytes/file object
            imageFile = io.BytesIO()
            # Convert Image object to bytes/file object
            image.save(imageFile, "JPEG")
            imageFile.seek(0)

            # Set file's name
            imageFile.name = newPhotoName
            # Create the files object to pass
            files = {"file" : imageFile}
            # Post the picture to the proper Employee
            response = req.post(url + "pictures/" + str(empID) + "/", files=files)
            
            cv2.imshow('image', img)

        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27: break

        elif photoNum >= frameCount: 
            print("\nFacial Scan Complete!\n")
            break

    # disconnects camera
    cam.release()
    cv2.destroyAllWindows()

    photoRegister.append(person)
    writePhotoRegister()
    recordLastScan(int(empID))
    trainDataset()
  

# Removes the facial recog data and database info of a specified employee
def removeEmployee():

    global photoRegister
    photoRegister = readPhotoRegister()
    flag = False

    while (flag == False):

        delEmpID = int(input("Enter the ID of the the employee to remove (-1 to quit):  "))
        if delEmpID == -1: flag = True

        for person in photoRegister:
            extractEmpID = int(person[1].split("_")[0])
        
            if delEmpID == extractEmpID:
                print("Removing Employee ID: "+str(extractEmpID)+" Pictures . . .")
                for pic in person: 
                    response = req.delete(url + "employees/" + str(extractEmpID) + "/")
                os.system("rm trainer/trainer.yml")
                photoRegister.remove(person)
                writePhotoRegister()
                print("Removed Employee ID: ", extractEmpID, " successfully!\n")
                flag = True
    
        if flag == False: 
            print("Employee ID not found!")


# Trains images in the dataset, outputs an updated .yml file to the trainer/ directory
def trainDataset():

    global photoRegister
    photoRegister = readPhotoRegister()

    if len(photoRegister) > 0:

        path = 'dataset'
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier("Cascades/haarcascade_frontalface_default.xml")

        def getImagesAndLabels(path):
            imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
            faceSamples = []
            ids = []
            for imagePath in imagePaths:
                PIL_img = Image.open(imagePath).convert('L')
                img_numpy = np.array(PIL_img,'uint8')
                id = int(os.path.split(imagePath)[-1].split("_")[0])
                print(id)
                faces = detector.detectMultiScale(img_numpy)
                for (x,y,w,h) in faces:
                    faceSamples.append(img_numpy[y:y+h,x:x+w])
                    ids.append(id)
            return faceSamples,ids

        print ("\n [INFO] Training faces . . .")
        faces,ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))
        recognizer.write('trainer/trainer.yml')
        print("\n Training complete !")

    else: print("\nNo Registered Employees!\n")


# Detects and identifies registered employee faces
def searchFace():

    global photoRegister
    photoRegister = readPhotoRegister()

    if len(photoRegister) > 0:

        trainDataset()

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        cascadePath = "Cascades/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath);
        font = cv2.FONT_HERSHEY_SIMPLEX

        # CAMERA INITIALIZATION
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # widht
        cam.set(4, 480) # height

        # face size threshold
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)

        print("Press 'ESC' key to exit\n")

        count = 0
        accuracyList = []

        while True:
            
            ret, img = cam.read()
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            
            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
            )

            for(x,y,w,h) in faces: # detects face

                EmpID, accuracy = recognizer.predict(gray[y:y+h,x:x+w]) # recognizes face
                
                accuracy = round(100 - accuracy)
                    
                if (accuracy <= 100) and (accuracy > 0):

                    if (count < 10):
                        accuracyList.append(accuracy)
                        avgAccuracy = -1
                        count += 1
                        print("taking accuracy")
                    elif (count >= 10):
                        avgAccuracy = np.average(accuracyList)
                        print("averaging accuracy", avgAccuracy)
                        accuracyList = [accuracy] + accuracyList
                        accuracyList.pop()

                else:
                    count = 0
                    accuracyList = []
                    avgAccuracy = -1

                # Checks accuracy average  
                if (avgAccuracy > 25):

                    response = req.get(url + "employees/" + str(EmpID) + "/")
                    name = response.json()['first_name'] + " " + response.json()['last_name'][0] + "."

                    cv2.circle(img, (int(x+(w/2)),int(y+(h/2))), 108, (0,220,0), 3)
                    cv2.putText(img, name, (x+w+25,int(y+(h/2))), font, 1, (255,255,0), 2)
                    cv2.putText(img, "Accy: "+str(avgAccuracy), (x+w+25,int(y+(h/2))+30), font, .75, (255,255,0), 2)

                    for person in photoRegister:
                        extractEmpID = (person[1].split("_"))[0]

                        if (int(extractEmpID) == EmpID):

                            lastScan = list(map(int, person[0].split(":")))
                            getDate = datetime.utcnow().date()
                            currentDate = [int(getDate.year), int(getDate.month), int(getDate.day)]

                            sameDay = (lastScan == currentDate)
                            dayDiff = np.abs(currentDate[2] - lastScan[2])


                            if not sameDay:
                            
                                print("UPDATING  . . .")
                                for i in range(updateFrameCount): # updates employee photos

                                    photoName = RegisterShift(EmpID)

                                    response = req.delete(url + "pictures/" + photoName + "/")
                                    # Convert captured frame to Image object
                                    image = Image.fromarray(gray[y:y+h,x:x+w])
                                    imageFile = io.BytesIO()
                                    image.save(imageFile, "JPEG")
                                    imageFile.seek(0)
                                    imageFile.name = photoName + ".jpg"
                                    files = {"file" : imageFile}
                                    if photoName != "none":
                                        response = req.post(url + "pictures/" + str(EmpID) + "/", files=files) # add newly captured photo
                                    
                                recordLastScan(EmpID) # logs last face scan time
                                
                else:
                    cv2.circle(img, (int(x+(w/2)),int(y+(h/2))), 108, (0,0,255), 3) 
                    cv2.putText(img, "Scanning", (x+w+25,int(y+(h/2))+30), font, .75, (255,255,255), 2) 
                
            cv2.imshow('camera',img)
            
            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break

        cam.release()
        cv2.destroyAllWindows()
        return()

    else: print("\nNo Registered Employees!\n")


# Function still in testing
# Takes in photoID to index person
# Adds new and removes old photos
# This is used to maintain an updated register of each person's face as they interact with the camera
def RegisterShift(empID):

    global photoRegister, frameCount
    photoRegister = readPhotoRegister()
    maxPhotoAmnt = frameCount # define the number of photos of a single person to be kept 

    for person in photoRegister:
        extractEmpID = (person[1].split("_"))[0]

        if int(extractEmpID) == empID:
            
            tempPic = person[-1] # copies a person's last picture name
            person.remove(person[-1]) # removes person's last picture name

            person.insert(1, tempPic) # inserts copy at front
            writePhotoRegister()

            return(tempPic)
    

def main():

    print("GreeterGuru : FaceID Funcionality testing\n\n")

    action = 0
    while (action != -1):

        # Test action menu
        print("ACTIONS:\n",
            "1. Register new employee\n", 
            "2. Run operation mode\n", 
            "[-1] to QUIT\n") 

        action = int(input("Select an action:"))

        if action == 1: 
            createEmployee()
        elif action == 2:
            searchFace()
        elif action == -1:
            print("Exiting Program")
        else: print("\nEnter correct value\n")

main()
