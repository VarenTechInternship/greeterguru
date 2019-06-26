#from workflow.views import *
from django.test import LiveServerTestCase
import requests


class viewTests(LiveServerTestCase):

    def test_create_employee(self):

        url = str(self.live_server_url) + "/api/"

        data = {
            "first_name":"Kendall",
            "last_name":"Kempton",
            "emp_ID":500,
            "emp_email":"kemptonk@varentech.com",
            "manager_email":"parksw@varentech.com",
            "keycode":12345,
            "emp_permissions":1,
            "last_login":"19-06-26",
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
            "emp_permissions":1,
            "last_login":"19-06-26",
        }
        
        try:
            response = requests.post(url + "employees/", json=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
