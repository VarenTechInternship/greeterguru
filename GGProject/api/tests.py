from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from workflow.models import Employee
from workflow.serializers import EmployeesSerializer


# Creates API test case
class BaseViewTest(APITestCase):
    
    client = APIClient()

    # Method for creating employees
    @staticmethod
    def create_employee(first_name="", last_name="", primary_key=None, authen=None):
        if first_name != "" and last_name != "" and  primary_key!=None and authen!=None:
            Employee.objects.create(first_name=first_name, last_name=last_name, primary_key=primary_key, authen=authen)

    # Initialize four employees
    def setUp(self):
        self.create_employee("kendall", "kempton", 565, 0)
        self.create_employee("jay", "hall", 560, 0)
        self.create_employee("caroline", "orndorff", 335, 0)
        self.create_employee("will", "parks", 104, 1)

        
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
