# !/usr/bin/python
# funcTest.py
# TESTS THE VARIOUS FACEID FUNCTIONS
#-----------------------------------

# LIBRARIES
import cv2
import os
import sys
import numpy as np
from PIL import Image


# CAMERA SETUP
#cam = cv2.VideoCapture(0)
#cam.set(3, 640) # set video width
#cam.set(4, 480) # set video height

# FACE DETECTION MODEL
face_detector = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')


# GLOBAL VARIABLES : FOR TESTING PURPOSES -------------------------------------------

# Stores photo names for each person as a 2D list
# In imlpementation, this will be accessed from a text file
testPhotoRegister = []
photoRegister = []


def readPhotoRegister():

    # takes in nothing
    # returns 2D list
    global photoRegister
    photoNames = open("photoNames.txt", "r")
    photoRegister = photoNames.readlines()

    for i in range(len(photoRegister)):
        person = photoRegister[i]
        person = person.strip().split(",")
        #print(person)
        photoRegister[i] = person
    photoNames.close()

    return(photoRegister)


# takes in updated photoRegister
# writes to txt file
def writePhotoRegister():

    global photoRegister
    photoNames = open("photoNames.txt", "w")

    # delete contents first
    photoNames.truncate()

    copy = []
    for person in photoRegister:
        line = ",".join(person)
        copy.append(line)
        photoNames.write(line)

    photoNames.close()


def createEmployee():

    # 1. get employee ID
    # 2. take frames
    # 3. append person to photoRegister --> [employeeID] + [photo#]
    # 4. add to dataset/ folder & send to database

    global photoRegister
    #photoRegister = readPhotoRegister()
    #person = [] # an index inside of the 'photoRegister[]' list
    #photoNum = len(photoRegister)
    photoNum = 0 # an index inside of the 'person[]' list
    frameCount = 50

    flag = False
    while flag == False:

        empID = input("Enter your EMPLOYEE ID:  ") # get employee ID

        if len(photoRegister) == 0:
            flag = True

        for person in photoRegister:
            # get the empID --> check if equal to input
            extractEmpID = (person[0].split("_"))[0]

            if extractEmpID == empID:
                print("Employee already exists")
            else: flag = True

    # CAMERA SETUP
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height
    person = []

    while(True):

        # get camera feed in gray
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(gray, 1.3, 5) # detects face

        # only while face is detected
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2) # draw rectangle around face
            photoNum += 1 # increment index

            newPhotoName = str(empID) + '_' + str(photoNum) + ".jpg"

            cv2.imwrite("dataset/" + newPhotoName, gray[y:y+h, x:x+w]) # saves photo to 'dataset/' using naming convention
            person.append(newPhotoName.strip(".jpg"))
            # { upload to database here !! }

            cv2.imshow('image', img) # display image

        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        # stop when frameCount is satisfied
        elif photoNum >= frameCount:
            print("\nFacial Scan Complete!\n")
            break

    photoRegister.append(person) # add person to list
    writePhotoRegister()
    trainDataset() # train dataset

    # disconnect camera
    cam.release()
    cv2.destroyAllWindows()


def removeEmployee():

    global photoRegister
    photoRegister = readPhotoRegister()
    print(photoRegister)

    delEmpID = int(input("Enter the ID of the the employee to remove:  \n"))

    for person in photoRegister:

        extractEmpID = int(person[0].split("_")[0])
        print(extractEmpID)

        if delEmpID == extractEmpID:

            for pic in person:

                # If file exists, delete it ##
                #if os.path.isfile("/testDataset/"+pic):
                #    os.remove("/testDataset/"+pic)
                #os.remove(r"dataset/"+pic)
                os.system("rm dataset/" + str(pic) + ".jpg")
                #with open("dataset/"+pic+".jpg") as file
                #    os.remove(file)
                print(pic)

            #os.remove(r"dataset/"+str(extractEmpID)+"*")
            photoRegister.remove(person)
            print("Removed Employee with ID: ", extractEmpID, " successfully!\n")
        print("tick")
        writePhotoRegister()



def trainDataset():

    path = 'dataset'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("Cascades/haarcascade_frontalface_default.xml")

    # function to get the images and label data
    def getImagesAndLabels(path):

        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples=[]
        ids = []

        for imagePath in imagePaths:

            PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
            img_numpy = np.array(PIL_img, 'uint8')
            #id = int(os.path.split(imagePath)[-1].split(".")[1])
            id = int(os.path.split(imagePath)[-1].split("_")[0]) # gets the
            print(id)
            faces = detector.detectMultiScale(img_numpy)

            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y+h, x:x+w])
                ids.append(id)

        return faceSamples,ids

    print("\n [INFO] Training faces . . .")
    faces,ids = getImagesAndLabels(path)
    recognizer.train(faces, np.array(ids))

    # Save the model into trainer/trainer.yml
    recognizer.write('trainer/trainer.yml')
    print("\n Training complete !")


# takes in photoID to index person
# adds new and removes old photos
def RegisterShift():

    global photoRegister
    readPhotoRegister()
    maxPhotoAmnt = 10 # define the number of photos of a single person to be kept

    # FIND FACE, THEN . . . ***
    person = testPhotoRegister[photoID] # grab the person via photoID
    temp = person[-1] # copies a person's last picture name
    person.remove(len(person)) # removes person's last picture name
    # remove actual photo with name 'person[-1]' --> os.remove("/testDataset/person[-1]")
    person.insert(0, temp) # inserts copy at front
    photoRegister[photoID] = person # re-assign the updated photo names to that person

    # save new photo with name 'temp'
    writePhotoRegister()



def searchFace():

    # look for face
    # return id & confidence
    # return false if nothing

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "Cascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX

    #iniciate id counter
    photoID = 0
    global PhotoRegister
    readPhotoRegister()

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:

        ret, img = cam.read()
        #img = cv2.flip(img, -1) # Flip vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )
        # print(faces)

        # Only runs while a face is detected
        for(x,y,w,h) in faces:

            photoID, confidence = recognizer.predict(gray[y:y+h,x:x+w]) # GETS 'PERSON' ??? AND CONFIDENCE
            print(photoID, 100 - confidence)
            '''
            person = testPhotoRegister[photoID]
            if len(person>0):
                extractEmpID = person[0].split("_")[0]
            '''

            # Check if confidence is less them 100 ==> "0" is perfect match
            if ((confidence < 100) and (100 - confidence) > 25):
                msg = str(photoID)
                confidence = "{0}%".format(round(100 - confidence))
                #cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 6) # outlines face with rectangle
                cv2.circle(img, (int(x+(w/2)), int(y+(h/2))), 108, (50,0,0), 3)
                cv2.putText(img, "EmpID: " + msg, (x+w+25, int(y+(h/2))), font, 1, (255, 255, 0), 2) # prints person's employee ID
                cv2.putText(img, "conf: " + str(confidence), (x+w+25, int(y+(h/2))+30), font, 0.75, (255, 255, 0), 2)  # prints confidence level
            else:
                msg = "???"
                confidence = "{0}%".format(round(100 - confidence))
                #cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 6) # outlines face with rectangle
                cv2.circle(img, (int(x+(w/2)), int(y+(h/2))), 108, (0, 0, 255), 3)
                cv2.putText(img, "EmpID: " + msg, (x+w+25, int(y+(h/2))), font, 1, (255, 255, 255), 2) # prints person's employee ID
                cv2.putText(img, "conf: " + str(confidence), (x+w+25, int(y+(h/2))+30), font, 0.75, (255, 255, 255), 2)  # prints confidence level

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
    return()




def main():

    print("GreeterGuru : Funcionality testing\n\n")

    action = 1
    while (action >= 1 and action <= 3) or (action != -1):

        print("ACTIONS:\n","1. Register new employee\n", "2. Run operation mode\n", "3. Train Dataset", "4. 'Midnight Updates'\n", "[-1] to QUIT\n") # menu
        action = int(input("Select an action:"))
        facesTrained = False

        if action == 1:
            createEmployee()
        elif action == 2:
            # 1. trainDataset()
            # 2. detect a face --> recognized?
            #    yes: print("found", empID)
            #    no: continue scanning --> implement 'sleep camera' feature later
            # 3. if face recognized, capture 'frameCount' of frames and update dataset/ folder & photoRegister
            trainDataset()
            searchFace()
        elif action == 3:
            trainDataset()
            # train dataset
        elif action == 4:
            removeEmployee()
            # scheduled update sequence
        elif action == 5:
            photoRegister = readPhotoRegister()

            for person in photoRegister:
                print(",".join(person))
    # WHEN PERSON IDENTIFIED --> UPDATE THEIR PHOTOREGISTER****************



    # AT A GIVEN TIME (MIDNIGHT) --> DO . . . *****************************
    # - INITIATE ACTIVE DIR UPDATE
    # - TRAIN UPDATED FACES


main()
