import requests, json, getpass
from django.core.files import File


# Create authentication header containing admin token
def authenticate():

    # Set admin information
    username = "admin"
    password = getpass.getpass(prompt="Admin Password: ")
    data = {
        "username": username,
        "password": password,
    }

    # Retrieve token and create authentication header
    response = requests.post("http://localhost:8000/api/token-auth/", json=data)
    content = response.json()
    token = content["token"]
    headers = {'Authorization':'Token ' + token}

    return headers


# Retrieve and display all employees
def display_employees():

    # Retrieve all employees
    response = requests.get("http://localhost:8000/api/employees/")
    content = response.json()

    # Display all employees
    for person in content:
        for key in person:
            print(key + ":", person[key])
        print()

    return content


# Add employee object to database
def create_employee():

    # Define employee data
    data = {
        "first_name": "Jaylan",
        "last_name": "Hall",
        "emp_ID": 400,
        "emp_email": "hallj@varentech.com",
        "manage_email": "parksw@varentech.com",
        "keycode": 12345,
        "emp_permissions": '1',
        "last_login":"2019-06-26",
    }

    # Attempt to create employee object
    try:
        response = requests.post("http://localhost:8000/api/employees/", json=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)

    return response


# Display whether a request was successful
def verify(response):
    if response:
        print("SUCCESS!")
    else:
        print("whoops...")


def main():

    #response = create_employee()
    #verify(response)
    display_employees()

    pic_name = "500_0.jpg"
    files = {"file" : open(pic_name, 'rb')}
    try:
        response = requests.post("http://localhost:8000/api/pictures/500/", files=files)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)

main()
