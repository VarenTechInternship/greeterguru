import requests
import json
from getpass import getpass

def main():
    response = requests.get("http://localhost:8000/api/employees/")
    content = response.json()

    for person in content:
        for key in person:
            print(key + ":", person[key])
        print()


    #emp = requests.get("http://localhost:8000/api/employees/300/")
    #emp = emp.json()


    task = {"picture": "cat.jpg", "name": "cat.jpg"}
    response = requests.post("http://localhost:8000/api/pictures/400/")

    #content = response.json()

    """
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

    response = requests.put("http://localhost:8000/api/employees/450/", json=task)
    """
    if response:
        print("Success!")
    else:
        print("Whoops.")
    
main()
