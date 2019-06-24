from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Employee
from .serializers import EmployeesSerializer


# Creates API test case
class BaseViewTest(APITestCase):

    client = APIClient()

    # Method for creating employees
    @staticmethod
    def create_employee(first_name = "", last_name = "", emp_ID = None, emp_email = "", emp_permissions = None, manager_email = "", key_code = None):
        if first_name != "" and last_name != "" and  emp_ID != None and emp_permissions != None, and manager_email != "" and key_code != None:
            Employee.objects.create(first_name = first_name, last_name = last_name, emp_ID = emp_ID, emp_email = emp_email, emp_permissions = emp_permissions, manager_email = manager_email, key_code = key_code)


    # Initialize four employees & two admins
    def setUp(self):
        self.create_employee("kendall", "kempton", 565, "kemptonk@varentech.com", 2, "orndorffc@varentech.com", 12345)
        self.create_employee("jay", "hall", 560, "hallj@varentech.com", 2, "orndorffc@varentech.com", 12345)
        self.create_employee("caroline", "orndorff", 335, "orndorffc@varentech.com", 2, "orndorffc@varentech.com", 12345)
        self.create_employee("will", "parks", 104, "parksw@varentech.com", 2, "orndorffc@varentech.com", 12345)



# Run API test case
class GetAllEmployeesTest(BaseViewTest):

    # Method for ensuring all employees exist
    def test_get_all_employees(self):

        # Access the API endpoint
        response = self.client.get(
            reverse("employees-all", kwargs={"version": "v1"})
        )

        # Fetch data from db
        expected = Employee.objects.all()
        serialized = EmployeesSerializer(expected, many=True)

        # Verify retrieved data
        self.assertEqual(response.data, serialized.data)
        # Verify successful retrieval
        self.assertEqual(response.status_code, status.HTTP_200_OK)
