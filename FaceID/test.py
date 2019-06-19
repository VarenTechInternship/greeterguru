import requests
import json
from getpass import getpass

def main():
    # Retrieve all employees and display their information
    response = requests.get("http://localhost:8000/api/employees/")
    content = response.json()

    for person in content:
        for key in person:
            print(key + ":", person[key])
        print()


    # Attempt to post an image to the database
    # (Requires employee with emp_ID 400 to exist)
    """
    pic = open("cat.jpg", "r")
    task = {"picture": pic, "name": "cat"}
    response = requests.post("http://localhost:8000/api/pictures/400/", json=task)
    """

    """
    # Create employee object
    for person in content:
        for key in person:
            print(key + ":", person[key])
        print()
    """
    """   
    task = {
        "first_name": "Jaylan",
        "last_name": "Hall",
        "email": "hallj@varentech.com",
        "emp_ID": 400,
        "keycode": 12345,
    }

    response = requests.post("http://localhost:8000/api/employees/", json=task)
    """

    # Verify whether the request was successful
    if response:
        print("SUCCESS!")
    else:
        print("whoops...")
    
main()
