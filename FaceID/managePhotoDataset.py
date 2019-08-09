from datetime import datetime


# Reads contents of photoNames.txt file
def readPhotoNames():

    photoNamesFile = open("photoNames.txt", "r")
    photoNames = photoNamesFile.readlines()

    for i, photo in enumerate(photoNames):
        photoNames[i] = photo.strip().split(",")

    photoNamesFile.close()
    return(photoNames)


# Writes photoRegister content to photoNames.txt file
def writePhotoNames(photoRegister):

    photoNamesFile = open("photoNames.txt", "w")
    photoNamesFile.truncate()

    copy = []
    for person in photoRegister:
        line = ",".join(person)
        copy.append(line)
        photoNamesFile.write(line+"\n")

    photoNamesFile.close()


# Records time stamp for an employee
def recordLastScan(empID):

    photoRegister = readPhotoNames()

    # Make current time stamp
    currentDate = datetime.now().strftime("%Y:%m:%d")

    # Record time stamp to corresponding employee ID
    for person in photoRegister:
        extractEmpID = person[1].split("_")[0]
        if extractEmpID == str(empID):
            person[0] = currentDate
            break

    # Update photoNames.txt
    writePhotoNames(photoRegister)


# Maintains an updated register of each person's face as they interact with the camera
def registerShift(empID, frameCount):

    photoRegister = readPhotoNames()

    for person in photoRegister:
        extractEmpID = person[1].split("_")[0]

        # Remove old pic and add new pic for employee ID
        if int(extractEmpID) == empID:

            tempPic = person[-1]
            person.remove(person[-1])
            person.insert(1, tempPic)
            writePhotoNames(photoRegister) # update photoRegister
            return(tempPic) # returns pic name
