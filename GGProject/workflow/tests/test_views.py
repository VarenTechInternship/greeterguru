from django.test import TestCase, Client
import unittest
from workflow.models import Employee, Picture, TempPhoto
from django.urls import reverse
from workflow.views import ListEmployees, SingleEmployee, ListPictures, SinglePicture

class EmployeeViewsTestCase(TestCase):
    def test_all_employees(self):
        self.client = Client()

        emp1 = Employee.objects.create(
        first_name = 'a',
        last_name = 'b',
        emp_ID = 1
        )
        emp2 = Employee.objects.create(
        first_name = 'c',
        last_name = 'd',
        emp_ID = 2
        )

        resp = self.client.get('/workflow/employee/')
        self.assertEqual(resp.status_code, 302)

        self.assertEqual(emp1.first_name, 'a' )
        self.assertEqual(emp1.last_name, 'b')
