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
import json
from django.core.files import File
# For testing the server is local
url = "http://localhost:8000/api/"

from pad4pi import rpi_gpio
import I2C_LCD_driver
sys.path.append(os.path.join(os.environ["GGPATH"], "GGProject"))
from GreeterGuru import settings

# comment out for ubuntu --> uncomment for raspi
from gpiozero import MotionSensor
pir = MotionSensor(4)

# GLOBAL VARIABLES
photoRegister = [] # Stores photo names for each person as a 2D list
frameCount = 20 # the amount of frames to take and maintain for an employee
updateFrameCount = 5 # amount of frames to capture and update to a recognized employee
dayLim = 1 # [HOURS, MINS, SECS] --> the amount of time for the system to wait until updating that employee's photos again

# loads face detection model
face_detector = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

# Keypad layout
KEYPAD = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]
COL_PINS=[17, 15, 14, 4]
ROW_PINS=[24, 22, 27, 18]

# Initialize keypad and register the keypress handler
factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad = KEYPAD, row_pins = ROW_PINS, col_pins = COL_PINS)

# Whether the keypad should be accepting input
acceptInput = False
# Sequence of input keypresses
code = ""
# Variable used to update screen display
mylcd = I2C_LCD_driver.lcd()

# Retrieve authorization token for api and create header
data = {"username":"admin", "password":"V@r3nTech#"}
response = req.post(url + "token-auth/", json=data)
response.raise_for_status()
token = response.json()["token"]
headers = {"Authorization": "Token " + token}


# Handler function for the keypad
def handleKeyPress(key):

    global acceptInput
    global code

    # Add the pressed key to the code sequence when
    # input is being accepted
    if acceptInput and key != "#":
        print(key)
        code += key
        
    # Stop accepting input when the end key is pressed
    elif acceptInput and key == "#":
        acceptInput = False

keypad.registerKeyPressHandler(handleKeyPress)


# Retrieve input from the keypad
def getInput(sec):

    global acceptInput

    acceptInput = True
    endTime = time.time() + sec

    # Allow input to be accepted for sec seconds and
    # stop when the end key is pressed
    while acceptInput and time.time() < endTime:
        pass
    acceptInput = False

    # Return whether the loop ended because time ran out
    return (time.time() > endTime)


# Retrieves and verifies the keycode
def getKeycode(response):

    global mylcd
    global code

    # Retrieve the employee's actual keycode
    employee = response.json()
    actualKeycode = employee["keycode"]

    attempts = 0
    enteredKeycode = -1
    timeOut = False

    # Accept keycode attempts while the most recently entered one is incorrect,
    # there have been less than 3 attempts, and the input has not timed out
    while str(actualKeycode) != enteredKeycode and attempts < 3 and not timeOut:

        attempts += 1
        mylcd.lcd_display_string("Please enter", 1, 2)
        mylcd.lcd_display_string("keycode", 2, 4)

        # Allow keycode to be entered and determine whether the input timed out
        timeOut = getInput(10)
        enteredKeycode = code
        code = ""
        mylcd.lcd_clear()

        # Display if the entered keycode was incorrect
        if str(actualKeycode) != enteredKeycode and not timeOut:
            mylcd.lcd_display_string("Incorrect", 1, 3)
            mylcd.lcd_display_string("keycode", 2, 4)
            time.sleep(1.2)
            mylcd.lcd_clear()

    # Display if the input timed out and return error value
    if timeOut:
        mylcd.lcd_display_string("Input has", 1, 3)
        mylcd.lcd_display_string("timed out", 2, 3)
        time.sleep(1.2)
        mylcd.lcd_clear()
        return -1
    # Display welcome message and return verified emp_ID
    elif str(actualKeycode) == enteredKeycode:
        first_name = employee["first_name"]
        mylcd.lcd_display_string("Welcome", 1, 4)
        mylcd.lcd_display_string(first_name, 2, (16 - len(first_name)) // 2)
        return employee["emp_ID"]
    # Display that there were too many failed attempts and return error value
    else:
        mylcd.lcd_display_string("Too many", 1, 4)
        mylcd.lcd_display_string("failed attempts", 2)
        time.sleep(1.2)
        mylcd.lcd_clear()
        return -1


# Retrieves and verifies the emp_ID
def getEmpID():

    global mylcd
    global code
    global url
    global headers

    attempts = 0
    response = False
    timeOut = False

    # Accept keycode attempts while the most recently entered one is incorrect,
    # there have been less than 3 attempts, and the input has not timed out
    while not response and attempts < 3 and not timeOut:

        attempts += 1
        mylcd.lcd_display_string("Please enter", 1, 2)
        mylcd.lcd_display_string("employee ID", 2, 2)

        # Allow emp_ID to be entered and determine whether the input timed out
        timeOut = getInput(10)
        enteredID = code
        code = ""
        mylcd.lcd_clear()
        
        response = req.get(url + "employees/" + str(enteredID) + "/", headers=headers)

        # Display if the entered ID was not found
        if not response and not timeOut:
            mylcd.lcd_display_string("Employee ID", 1, 2)
            mylcd.lcd_display_string("not found", 2, 3)
            time.sleep(1.2)
            mylcd.lcd_clear()


    # Display if the input timed out and return error value
    if timeOut:
        mylcd.lcd_display_string("Input has", 1, 3)
        mylcd.lcd_display_string("timed out", 2, 3)
        time.sleep(1.2)
        mylcd.lcd_clear()
        return -1
    # Retrieve and verify keycode if valid ID was input
    elif response:
        print("getKeycode")
        return getKeycode(response)
    # Display that there were too many failed attempts and return error value
    else:
        mylcd.lcd_display_string("Too many", 1, 4)
        mylcd.lcd_display_string("failed attempts", 2)
        time.sleep(1.2)
        mylcd.lcd_clear()
        return -1


# Handles when a detected face is not recognized
def unrecognizedFace():

    print("Unrecognized Face")

    global mylcd

    # Display that the face was not recognized
    mylcd.lcd_display_string("Face not", 1, 4)
    mylcd.lcd_display_string("recognized", 2, 3)
    time.sleep(1.2)
    mylcd.lcd_clear()

    # Get employee ID of unrecognized person by having them
    # enter it and verify it with their keycode
    result = getEmpID()
    time.sleep(1)
    mylcd.lcd_clear()
    return result


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
    response = req.post(url + "token-auth/", json=data)
    # Convert the response to a readable format
    content = response.json()
    # Extract the token
    token = content["token"]

    # Create a header for the HTTP request containing the token
    headers = {"Authorization" : "Token " + token}


# Registers a new employee
def createEmployee(empID):

    # 1. get employee ID
    # 2. take frames
    # 3. append person to photoRegister --> [employeeID] + [photo#]
    # 4. add to dataset/ folder & send to database

    global photoRegister
    global headers
    photoRegister = readPhotoRegister()

    global frameCount
    photoNum = 0
    
    """
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
    """

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
            response = req.post(url + "pictures/" + str(empID) + "/", files=files, headers=headers)

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
    global headers
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
                    response = req.delete(url + "employees/" + str(extractEmpID) + "/", headers=headers)
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
    global headers
    photoRegister = readPhotoRegister()

    if len(photoRegister) > 0:

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
        avgAccuracy = -1
        accThreshold = 25
        lock = True

        camWait = 10 # waits this amount of time in seconds to detect a face
        timeStamp = time.time()

        while (np.abs(int((time.time() - timeStamp))) < camWait):

            ret, img = cam.read()
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
            )


            for(x,y,w,h) in faces: # detects face

                timeStamp = time.time()

                EmpID, accuracy = recognizer.predict(gray[y:y+h,x:x+w]) # recognizes face

                accuracy = round(100 - accuracy)

                if (accuracy <= 100) and (accuracy > 0):

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

                # Checks accuracy average
                if (avgAccuracy > accThreshold):

                    if lock == True: # things to run once !
                        print("UNLOCKED")
                        lock = False

                    response = req.get(url + "employees/" + str(EmpID) + "/", headers=headers)
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

                                    response = req.delete(url + "pictures/" + photoName + "/", headers=headers)
                                    # Convert captured frame to Image object
                                    image = Image.fromarray(gray[y:y+h,x:x+w])
                                    imageFile = io.BytesIO()
                                    image.save(imageFile, "JPEG")
                                    imageFile.seek(0)
                                    imageFile.name = photoName + ".jpg"
                                    files = {"file" : imageFile}
                                    if photoName != "none":
                                        response = req.post(url + "pictures/" + str(EmpID) + "/", files=files, headers=headers) # add newly captured photo

                                recordLastScan(EmpID) # logs last face scan time

                else:

                    if lock == False: #things to run once !
                        print("LOCKED")
                        lock = True
                        employee = unrecognizedFace()

                        # Determine if employee exists in photo register
                        found = False
                        for emp in photoRegister:
                            extractedID = emp[1].split("_")[0]
                            if extractedID == str(employee):
                                found = True

                        if found:
                            #registerShift()
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
                                    response = req.post(url + "pictures/" + str(EmpID) + "/", files=files, headers=headers) # add newly captured photo

                            recordLastScan(EmpID) # logs last face scan time
                        else:
                            #initializeEmployee()
                            createEmployee(employee)

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


# Maintains an updated register of each person's face as they interact with the camera
def RegisterShift(empID):

    global photoRegister
    global frameCount
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

# Continuoulsy checks PIR sensor for motion
def proximitySensor():

    global pir

    while True:

        pir.wait_for_motion()
        print("PIR ping")
        searchFace()


def main():

    print("GreeterGuru : FaceID Funcionality testing\n\n")

    action = 0
    while (action != -1):

        # Test action menu
        print("1. Register new employee\n",
            "2. searchFace() \n",
            "3. Run proximity sensor\n"
            "[-1] to QUIT\n")

        action = int(input("Select an action:"))

        if action == 1:
            createEmployee()
        elif action == 2:
            searchFace()
        elif action == 3:
            proximitySensor()
        elif action == -1:
            print("Exiting Program")
        else: print("\nEnter correct value\n")

main()
