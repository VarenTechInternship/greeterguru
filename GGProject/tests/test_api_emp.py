from django.test import LiveServerTestCase
from workflow.models import Employee
import requests as req
import json


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
            "last_login":"2019-06-27",
        }

        try:
            response = req.post(url + "employees/", json=data)
            response.raise_for_status()
        except req.exceptions.HTTPError as err:
            print(err)

        data = {
            "first_name":"Caroline",
            "last_name":"Orndorff",
            "emp_ID":300,
            "emp_email":"orndorffc@varentech.com",
            "manager_email":"parksw@varentech.com",
            "keycode":54321,
            "emp_permissions":'2',
            "last_login":"2019-06-27",
        }
        
        try:
            response = req.post(url + "employees/", json=data)
            response.raise_for_status()
        except req.exceptions.HTTPError as err:
            print(err)


    # Retrieve and display all employees
    def get_all_employees(self):
        
        url = str(self.live_server_url) + "/api/"

        try:
            response = req.get(url + "employees/")
            response.raise_for_status()
        except req.exceptions.HTTPError as err:
            print(err)

        content = response.json()

        for employee in content:
            for key in employee:
                print(key + ":", employee[key])
            print()
                
        return response


    # Retrieve single employee based on ID
    def get_single_employee(self, emp_ID):

        url = str(self.live_server_url) + "/api/"

        try:
            response = req.get(url + "employees/" + str(emp_ID) + "/")
            response.raise_for_status()
        except req.exceptions.HTTPError as err:
            print(err)

        employee = response.json()

        for key in employee:
            print(key + ":", employee[key])
        print()

        return response
            

    # Change employee's ID
    def update_employee_ID(self, old_emp_ID, new_emp_ID):

        url = str(self.live_server_url) + "/api/"

        data = {
            "emp_ID":new_emp_ID,
        }

        try:
            response = req.put(url + "employees/" + str(old_emp_ID) + "/", json=data)
            response.raise_for_status()
        except req.exceptions.HTTPError as err:
            print(err)

        return response
        

    # Delete single employee
    def delete_employee(self, emp_ID):

        url = str(self.live_server_url) + "/api/"

        try:
            response = req.delete(url + "employees/" + str(emp_ID) + "/")
            response.raise_for_status()
        except req.exceptions.HTTPError as err:
            print(err)
            
        return response

    
    # Tests all employee API functionalities
    def test_employees(self):

        print()
        
        # Create two employees (emp_ID = 300, 500)
        self.create_employees()
        # Display all employees
        print("ALL EMPLOYEES, INITIAL:")
        self.get_all_employees()
        print()
        # Display employee 500
        print("EMPLOYEE 500, INITIAL:")
        self.get_single_employee(500)
        print()
        
        # Change emp_ID 500 to 600
        self.update_employee_ID(500, 600)
        # Display all employees
        print("EMPLOYEE 500, AFTER UPDATING EMP_ID TO 600:")
        self.get_single_employee(600)
        print()
        
        # Delete employee with ID 300
        self.delete_employee(300)
        # Display all employees
        print("ALL EMPLOYEES, AFTER DELETING EMPLOYEE 300:")
        self.get_all_employees()
        print()

        # Manually delete all Employee objects
        Employee.objects.all().delete()
