from django.test import LiveServerTestCase
from workflow.models import Employee
import requests as req
import json


class EmployeeTests(LiveServerTestCase):

    # Create employee object with passed data
    def create_employee(
        self,
        username,
        password,
        first_name,
        last_name,
        email,
        emp_ID,
        keycode,
        permissions,
    ):

        url = str(self.live_server_url) + "/api/"

        data = {
            "username":username,
            "password":password,
            "first_name":first_name,
            "last_name":last_name,
            "email":email,
            "emp_ID":emp_ID,
            "keycode":keycode,
            "permissions":permissions,
        }

        response = req.post(url + "employees/", json=data)
        response.raise_for_status()
        return response.json()


    # Retrieve all employees
    def get_all_employees(self):

        url = str(self.live_server_url) + "/api/"

        response = req.get(url + "employees/")
        response.raise_for_status()
        return response.json()


    # Retrieve single employee based on ID
    def get_single_employee(self, emp_ID):

        url = str(self.live_server_url) + "/api/"

        response = req.get(url + "employees/" + str(emp_ID) + "/")
        response.raise_for_status()
        return response.json()


    # Delete single employee
    def delete_employee(self, emp_ID):

        url = str(self.live_server_url) + "/api/"

        response = req.delete(url + "employees/" + str(emp_ID) + "/")
        response.raise_for_status()
        return response


    # Tests all employee API functionalities
    def test_employees(self):

        # Create employee 500
        self.create_employee(
            username="kemptonk",
            password="V@r3nTech#",
            first_name="Kendall",
            last_name="Kempton",
            email="kemptonk@varentech.com",
            emp_ID=500,
            keycode=12345,
            permissions="1",
        )

        # Create employee 300
        self.create_employee(
            username="orndorffc",
            password="V@r3nTech#",
            first_name="Caroline",
            last_name="Orndorff",
            email="orndorffc@varentech.com",
            emp_ID=300,
            keycode=54321,
            permissions="2",
        )

        # Verify the 2 employees were successfully created
        emp_all = self.get_all_employees()
        self.assertEqual(len(emp_all), 2)

        # Delete employee 300
        self.delete_employee(300)
        # Verify employee 300 was deleted
        emps = self.get_all_employees()
        self.assertEqual(len(emps), 1)

        # Manually delete all remaining Employee objects
        Employee.objects.all().delete()
