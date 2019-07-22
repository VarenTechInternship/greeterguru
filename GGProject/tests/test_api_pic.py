from django.test import LiveServerTestCase
from django.core.files import File
from GreeterGuru.settings import MEDIA_ROOT
from workflow.models import Employee, Picture
import requests as req
import json


# Requires files 300_0.jpg, 300_1.jpg, 500_0.jpg, and 500_1.jpg
# to be located at GreeterGuru/FaceID/TestPics/
class PictureTests(LiveServerTestCase):

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


    # Add picture to a specified employee
    def add_picture(self, emp_ID, pic_name):

        url = str(self.live_server_url) + "/api/"

        files = {"file" : open(pic_name, 'rb')}

        response = req.post(url + "pictures/" + str(emp_ID) + "/", files=files)
        response.raise_for_status()
        return response.json()


    # Retrieve all pictures
    def get_pictures(self):

        url = str(self.live_server_url) + "/api/"

        response = req.get(url + "pictures/")
        response.raise_for_status()
        return response.json()


    # Retrieve all pictures belonging to a given employee
    def get_emp_pictures(self, emp_ID):

        url = str(self.live_server_url) + "/api/"

        response = req.get(url + "pictures/" + str(emp_ID) + "/")
        response.raise_for_status()
        return response.json()


    # Retrieve  a single picture based on a name
    def get_single_picture(self, name):

        url = str(self.live_server_url) + "/api/"

        response = req.get(url + "pictures/" + name + "/")
        response.raise_for_status()
        return response.json()


    # Update a picture's name
    def update_picture_name(self, old_name, new_name):

        url = str(self.live_server_url) + "/api/"

        data = {
            "name": new_name,
        }

        response = req.put(url + "pictures/" + old_name + "/", json=data)
        response.raise_for_status()
        return response.json()


    # Delete a picture with a given name
    def delete_picture(self, name):

        url = str(self.live_server_url) + "/api/"

        response = req.delete(url + "pictures/" + name + "/")
        response.raise_for_status()
        return response


    # Test all of the Picture API functionalities
    def test_pictures(self):

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

        # Add two pictures to employee 300 and two to employee 500
        # After each addition, immediately verify the picture was name correctly
        pic = self.add_picture(300, MEDIA_ROOT + "TestPics/300_0.jpg")
        self.assertEqual(pic["name"], "300_0")
        pic = self.add_picture(300, MEDIA_ROOT + "TestPics/300_1.jpg")
        self.assertEqual(pic["name"], "300_1")
        pic = self.add_picture(500, MEDIA_ROOT + "TestPics/500_0.jpg")
        self.assertEqual(pic["name"], "500_0")
        pic = self.add_picture(500, MEDIA_ROOT + "TestPics/500_1.jpg")
        self.assertEqual(pic["name"], "500_1")

        # Verify all pictures were successfully added
        pic_all = self.get_pictures()
        self.assertEqual(len(pic_all), 4)

        # Separately retrieve pictures belonging to employees 300 and 500
        pic_300 = self.get_emp_pictures(300)
        pic_500 = self.get_emp_pictures(500)
        # Verify pictures were added to correct employees
        self.assertEqual(len(pic_300), 2)
        self.assertEqual(len(pic_500), 2)


        # Change picture 500_1 to 500_2
        pic = self.update_picture_name("500_1", "500_2")
        # Verify the name change
        self.assertEqual(pic["name"], "500_2")

        # Delete picture 300_1
        self.delete_picture("300_1")
        # Verify the picture was deleted
        pic_300 = self.get_emp_pictures(300)
        self.assertEqual(len(pic_300), 1)

        # Delete employee 300
        Employee.objects.get(emp_ID=500).delete()
        # Verify all the pictures belonging to them were deleted as well
        pic_all = self.get_pictures()
        self.assertEqual(len(pic_all), 1)

        # Manually delete all Employee objects
        # (This automatically deletes all picture objects)
        Employee.objects.all().delete()
