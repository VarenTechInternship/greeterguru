from django.test import LiveServerTestCase
from workflow.models import Employee
import requests as req
import json


# Only necessary if authen in workflow/views.py is set to IsAdminUser
class AuthenticateTests(LiveServerTestCase):

    # Attempt to access the API unauthenticated
    def unauthenticated(self):

        url = str(self.live_server_url) + "/api/"

        data = {
            "first_name":"Kendall",
            "last_name":"Kempton",
            "emp_ID":500,
        }

        try:
            response = req.post(url + "employees/", json=data)
            response.raise_for_status()
        except req.exceptions.HTTPError as err:
            print(err)


    # Attempt an unauthenticated requests
    def test_authenticate(self):

        # Attempt an unauthorized request
        print("SHOULD PRINT 401 ERROR:")
        self.unauthenticated()

        Employee.objects.all().delete()
