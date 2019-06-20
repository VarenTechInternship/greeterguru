# funcTest.py
# TESTS THE VARIOUS FACEID FUNCTIONS
#-----------------------------------

# LIBRARIES
import cv2
import os

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


def createEmployee():

    # 1. get employee ID
    # 2. take frames 
    # 3. append person to photoRegister --> [employeeID] + [photo#]
    # 4. add to dataset/ folder & send to database

    global testPhotoRegister 
    person = [] # an index inside of the 'photoRegister[]' list
    #photoNum = len(photoRegister)
    photoNum = 0 # an index inside of the 'person[]' list
    frameCount = 10

    empID = input("Enter your EMPLOYEE ID:  ") # get employee ID
    flag = False
    while flag==False:
        if len(testPhotoRegister)==0:
            break
        for person in testPhotoRegister:
            # get the empID --> check if equal to input
            extractEmpID = person[0].split("_")[0]
            if extractEmpID==empID:
                print("Employee already exists")
                empID = input("Enter your EMPLOYEE ID:  ") # get employee ID
            else: flag = True

    # CAMERA SETUP
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height

    while(True):

        # CAMERA SETUP
        #cam = cv2.VideoCapture(0)
        #cam.set(3, 640) # set video width
        #cam.set(4, 480) # set video height
    
        # get camera feed in gray
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(gray, 1.3, 5) # detects face

        # only while face is detected
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2) # draw rectangle around face
            photoNum += 1 # increment index 

            newPhotoName = str(empID) + '_' + str(photoNum) + ".jpg"

            cv2.imwrite("testDataset/"+newPhotoName, gray[y:y+h,x:x+w]) # saves photo to 'dataset/' using naming convention
            person.append(newPhotoName)
            testPhotoRegister.append(person)
            # { upload to database here !! }

            cv2.imshow('image', img) # display image

        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27: break

        # stop when frameCount is satisfied
        elif photoNum >= frameCount: 
            print("\nFacial Scan Complete!\n")
            break

    cam.release()
    cv2.destroyAllWindows()



"""
def updateRegister(photoID):

    maxPhotoAmnt = 3 # define the number of photos of a single person to be kept 

    person = testPhotoRegister[photoID]
    temp = person[-1]
    person.remove(len(person))
    person.insert(0, temp)

    photoRegister[photoID] = person

    return(photoRegister)

def searchFace():

    # look for face
    # return id & confidence
    # return false if nothing

    return()

"""


def main():

    print("GreeterGuru : Funcionality testing\n\n")

    action = 1
    while (action>=1 and action<=3) or (action!=-1):

        print("ACTIONS:\n","1. Register new employee\n", "2. Run operation mode\n", "3. 'Midnight Updates'\n", "[-1] to QUIT\n") # menu
        action = int(input("Select an action:"))

        if action ==1:
            createEmployee()

    # WHEN PERSON IDENTIFIED --> UPDATE THEIR PHOTOREGISTER****************



    # AT A GIVEN TIME (MIDNIGHT) --> DO . . . *****************************
    # - INITIATE ACTIVE DIR UPDATE
    # - TRAIN UPDATED FACES


main()

