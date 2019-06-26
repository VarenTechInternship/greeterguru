from workflow.models import Employee, Picture, TempPhoto
import unittest

class EmployeeTestCase(unittest.TestCase):
    def setUp(self):
        Employee.objects.create(
            first_name = "Kendall",
            last_name = "Kempton",
            emp_ID = 500,
            emp_email = "kemptonk@varentech.com",
            manager_email = "parksw@varentech.com",
            keycode = 12345,
            emp_permissions = '1',
            last_login = "2019-06-26",
        )

        Employee.objects.create(
            first_name = "Caroline",
            last_name = "Orndorff",
            emp_ID = 300,
            emp_email = "orndorffc@varentech.com",
            manager_email = "parksw@varentech.com",
            keycode = 54321,
            emp_permissions = '1',
            last_login = "2019-06-26",
        )

