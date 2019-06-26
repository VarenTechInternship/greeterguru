from django.test import TestCase, Client
import unittest
from workflow.models import Employee, Picture, TempPhoto

#employee model test
class EmployeeTest(TestCase):
    client = Client()
    def create_employee(self,
        first_name = 'a',
        last_name = 'b',
        emp_ID = 1,
        emp_email = 'c@varentech.com',
        manager_email = 'd@varentech.com',
        keycode = 12345,
        emp_permissions = '1',
        login_time = '2018-01-01'):
        return Employee.objects.create(
        first_name = first_name,
        last_name = last_name,
        emp_ID = emp_ID,
        emp_email = emp_email,
        manager_email = manager_email,
        keycode = keycode,
        emp_permissions = emp_permissions,
        login_time = login_time)

    def test_employee_creation(self):
        client = Client()
        a = self.create_employee()
        self.assertTrue(isinstance(a, Employee))
        self.assertEqual(a.__str__(), a.first_name + ' ' + a.last_name)
