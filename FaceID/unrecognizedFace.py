import time
import sys
import os
import requests as req
import json
import I2C_LCD_driver
from pad4pi import rpi_gpio
# Add web app directory to system path in order to import its settings
sys.path.append(os.path.join(os.environ["GGPATH"], "GGProject"))
from GreeterGuru import settings



# Whether the keypad should be accepting input
acceptInput = False
# Sequence of input keypresses
code = ""
# Variable used to update screen display
mylcd = I2C_LCD_driver.lcd()


# Handler function for the keypad
def handleKeyPress(key):

    global acceptInput
    global code

    # Add the pressed key to the code sequence when
    # input is being accepted
    if acceptInput and key != "#":
        code += key
    # Stop accepting input when the end key is pressed
    elif acceptInput and key == "#":
        acceptInput = False
        

# Retrive input from the keypad
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

    # Url of the web app's api
    url = settings.WEB_URL + "api/"

    # Retrieve authorization token for api and create header
    data = {"username":"admin", "password":"V@r3nTech#"}
    response = req.post(url + "token-auth/", json=data)
    response.raise_for_status()
    token = response.json()["token"]
    header = {"Authorization": "Token " + token}
    
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
        
        # Attempt to retrieve employee object belonging to that ID
        response = req.get(url + "employees/" + enteredID + "/", headers=header)

        # Display if the employee was not found
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
    
    # Retrieve keycode if employee was found
    elif response:
        return getKeycode(response)
    # Display that there were too many failed attempts and return error value
    else:
        mylcd.lcd_display_string("Too many", 1, 4)
        mylcd.lcd_display_string("failed attempts", 2)
        time.sleep(1.5)
        mylcd.lcd_clear()
        return -1


def main():

    global mylcd

    # Keypad layout
    KEYPAD = [
        ["1", "2", "3", "A"],
        ["4", "5", "6", "B"],
        ["7", "8", "9", "C"],
        ["*", "0", "#", "D"]
    ]
    COL_PINS = [17, 15, 14, 4]
    ROW_PINS = [24, 22, 27, 18]

    # Initialize keypad and register the keypress handler
    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_keypad(keypad = KEYPAD, row_pins = ROW_PINS, col_pins = COL_PINS)
    keypad.registerKeyPressHandler(handleKeyPress)

    # Display that the face was not recognized
    mylcd.lcd_display_string("Face not", 1, 4)
    mylcd.lcd_display_string("recognized", 2, 3)
    time.sleep(1.2)
    mylcd.lcd_clear()

    # Get employee ID of unrecognized person by having them
    # enter it and verify it with their keycode
    result = getEmpID()
    print(result)
    time.sleep(1.2)
    mylcd.lcd_clear()

main()
