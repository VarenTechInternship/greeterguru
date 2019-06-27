from django.test import LiveServerTestCase
from django.core.files import File
import requests, json, getpass


class EmployeeTests(LiveServerTestCase):

    # Creates two employee objects
    def create_employees(self):

        url = str(self.live_server_url) + "/api/"

        data = {
            "first_name":"Kendall",
            "last_name":"Kempton",
            "emp_ID":500,
            "emp_email":"kemptonk@varentech.com",
            "manager_email":"parksw@varentech.com",
            "keycode":12345,
            "emp_permissions":'1',
            "last_login":"2019-06-26",
        }

        try:
            response = requests.post(url + "employees/", json=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)


        data = {
            "first_name":"Caroline",
            "last_name":"Orndorff",
            "emp_ID":300,
            "emp_email":"orndorffc@varentech.com",
            "manager_email":"parksw@varentech.com",
            "keycode":54321,
            "emp_permissions":'1',
            "last_login":"2019-06-26",
        }
        
        try:
            response = requests.post(url + "employees/", json=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)


    # Retrieve all employees
    def get_all_employees(self):
        
        url = str(self.live_server_url) + "/api/"

        try:
            response = requests.get(url + "employees/")
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)

        return response


    # Retrieve single employee based on ID
    def get_single_employee(self, emp_ID):

        url = str(self.live_server_url) + "/api/"

        try:
            response = requests.get(url + "employees/" + str(emp_ID) + "/")
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)

        return response
            

    # Change employee's ID
    def update_employee_ID(self, old_emp_ID, new_emp_ID):

        url = str(self.live_server_url) + "/api/"

        data = {
            "emp_ID":new_emp_ID,
        }

        try:
            response = requests.put(url + "employees/" + str(old_emp_ID) + "/",
                                    json=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)

        return response
        

    # Delete single employee
    def delete_employee(self, emp_ID):

        url = str(self.live_server_url) + "/api/"

        try:
            response = requests.delete(url + "employees/" + str(emp_ID) + "/")
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)

        return response

    
    # Tests all employee API functionalities
    # Should display two HTTP 400 errors
    def test_employees(self):

        # Create two empoyees (emp_ID = 300, 500)
        self.create_employees()
        # Retrieve both employees
        self.get_all_employees()
        
        # Fail to retrieve employee with emp_ID = 400
        self.get_single_employee(400)
        # Change emp_ID 500 to 400
        self.update_employee_ID(500, 400)
        # Successfully retrieve employee with emp_ID = 400
        self.get_single_employee(400)

        # Delete employee with ID 300
        self.delete_employee(300)
        # Fail to retrive employee with emp_ID = 300
        self.get_single_employee(300)
