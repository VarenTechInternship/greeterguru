from django.test import TestCase, Client
from django.urls import reverse
from workflow.models import Employee, Picture, TempPhoto
from django.conf.urls import url
from workflow import views
import unittest2


class EmployeeTests(TestCase):
    def setUp(self):
        Employee.objects.create(
            username = 'username',
            password = 'password',
            first_name = 'first name',
            last_name = 'last name',
            email = 'email@gmail.com',
            emp_ID = 1,
            keycode = 12345,
            permissions = '0',
        )

        Picture.objects.create(
            employee = Employee.objects.get(emp_ID = 1),
            picture = 'schematics.png',
            name = 'pic1'
        )

        TempPhoto.objects.create(
            temp_id = 1,
            unknown_photo = 'schematics.png',
            name = 'unknownpic1'
        )


    #TEST EMPLOYEE MODEL
    #Test that employe goes into db and saves info in correct columns
    def test_employee_content(self):

        response = self.client.get(reverse('employees'))
        employee = Employee.objects.get(emp_ID = 1)

        expected_object_uname = f'{employee.username}'
        self.assertEqual(expected_object_uname, 'username')
        
        expected_object_pword = f'{employee.password}'
        self.assertEqual(expected_object_pword, 'password')

        expected_object_fname = f'{employee.first_name}'
        self.assertEqual(expected_object_fname, 'first name')
        
        expected_object_lname = f'{employee.last_name}'
        self.assertEqual(expected_object_lname, 'last name')

        expected_object_email = f'{employee.email}'
        self.assertEqual(expected_object_email, 'email@gmail.com')

        expected_object_empid = f'{employee.emp_ID}'
        self.assertEqual(expected_object_empid, '1')

        expected_object_keycode = f'{employee.keycode}'
        self.assertEqual(expected_object_keycode, '12345')

        expected_object_permissions = f'{employee.permissions}'
        self.assertEqual(expected_object_permissions, '0')

        
    #test that employee info shows up on employee single view
    def test_single_emp_view(self):
        employee = Employee.objects.get(emp_ID = 1)
        response = self.client.get('/employees/1/')

        expected_object_uname = f'{employee.username}'
        self.assertEqual(expected_object_uname, 'username')
        
        expected_object_pword = f'{employee.password}'
        self.assertEqual(expected_object_pword, 'password')

        expected_object_fname = f'{employee.first_name}'
        self.assertEqual(expected_object_fname, 'first name')
        
        expected_object_lname = f'{employee.last_name}'
        self.assertEqual(expected_object_lname, 'last name')

        expected_object_email = f'{employee.email}'
        self.assertEqual(expected_object_email, 'email@gmail.com')

        expected_object_empid = f'{employee.emp_ID}'
        self.assertEqual(expected_object_empid, '1')

        expected_object_keycode = f'{employee.keycode}'
        self.assertEqual(expected_object_keycode, '12345')

        expected_object_permissions = f'{employee.permissions}'
        self.assertEqual(expected_object_permissions, '0')


    #test that all information shows up on all employees view
    def test_all_emp_view(self):
        response = self.client.get(reverse('employees'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'username' and 'password' and
                            'first name' and 'last name' and '1' and
                            'email@gmail.com' and 'manager@gmail.com' and
                            '12345' and '0')


    #TEST PICTURE MODEL
    #test that picture saved under employee id has the correct information
    def test_picture_list_view(self):
        response = self.client.get(reverse('allpictures'))
        picture = Picture.objects.get(employee = 1)
        employee = Employee.objects.get(emp_ID = 1)

        expected_picture_id = f'{picture.employee}'
        expected_picture_pic = f'{picture.picture}'
        expected_picture_name = f'{picture.name}'

        self.assertEqual(expected_picture_id, employee.__str__())
        self.assertEqual(expected_picture_pic, 'schematics.png')
        self.assertEqual(expected_picture_name, 'pic1')

    #test that all info shows up on single employee page
    def test_single_pic_view(self):
        response = self.client.get("/pictures/first name last name/")
        picture = Picture.objects.get(employee = 1)
        employee = Employee.objects.get(emp_ID = 1)

        expected_picture_id = f'{picture.employee}'
        expected_picture_pic = f'{picture.picture}'
        expected_picture_name = f'{picture.name}'

        self.assertEqual(expected_picture_id, employee.__str__())
        self.assertEqual(expected_picture_pic, 'schematics.png')
        self.assertEqual(expected_picture_name, 'pic1')

    #TEST TEMP PICTURE MODEL
    #test that temp photos are saved with all information
    def test_temp_location(self):
        response = self.client.get(reverse('alltempphotos'))
        temppic = TempPhoto.objects.get(temp_id = 1)

        expected_temp_id = f'{temppic.temp_id}'
        expected_temp_location = f'{temppic.unknown_photo}'
        expected_temp_name = f'{temppic.name}'

        self.assertEqual(expected_temp_id, '1')
        self.assertEqual(expected_temp_location, 'schematics.png')
        self.assertEqual(expected_temp_name, 'unknownpic1')

    def tearDown(self):
        Employee.objects.all().delete()
        Picture.objects.all().delete()
        TempPhoto.objects.all().delete()
