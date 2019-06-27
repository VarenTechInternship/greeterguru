from django.test import LiveServerTestCase
from django.core.files import File
from GreeterGuru.settings import MEDIA_ROOT
from workflow.models import Employee, Picture
import requests as req
import json


# Requires files 300_0.jpg, 300_1.jpg, 500_0.jpg, and 500_1.jpg 
# to be located at GreeterGuru/FaceID/TestPics/
class PictureTests(LiveServerTestCase):

    # Creates two employee objects
    def create_employees(self):

        url = str(self.live_server_url) + "/api/"

        data = {
            "first_name":"Kendall",
            "last_name":"Kempton",
            "emp_ID":500,
            "emp_email":"kemptonk@varentech.com",
            "manager_email":"parksw@varentech.com",
            "keycode":12345,
            "emp_permissions":'1',
            "last_login":"2019-06-26",
        }

        try:
            response = req.post(url + "employees/", json=data)
            response.raise_for_status()
        except req.exceptions.HTTPError as err:
            print(err)


        data = {
            "first_name":"Caroline",
            "last_name":"Orndorff",
            "emp_ID":300,
            "emp_email":"orndorffc@varentech.com",
            "manager_email":"parksw@varentech.com",
            "keycode":54321,
            "emp_permissions":'1',
            "last_login":"2019-06-26",
        }
        
        try:
            response = req.post(url + "employees/", json=data)
            response.raise_for_status()
        except req.exceptions.HTTPError as err:
            print(err)


    # Add picture to a specified employee
    def add_picture(self, emp_ID, pic_name):
        
        url = str(self.live_server_url) + "/api/"       

        files = {"file" : open(pic_name, 'rb')}
        try:
            response = req.post(url + "pictures/" + str(emp_ID) + "/", files=files)
            response.raise_for_status()
        except req.exceptions.HTTPError as err:
            print(err)

            
    # Retrieve and display all pictures
    def get_pictures(self):

        url = str(self.live_server_url) + "/api/"

        try:
            response = req.get(url + "pictures/")
            response.raise_for_status()
        except req.exceptions.HTTPError as err:
            print(err)

        content = response.json()

        for picture in content:
            for key in picture:
                print(key + ":", picture[key])
            print()
                
        return response

    
    # Retrieve and display all pictures belonging to a given employee
    def get_emp_pictures(self, emp_ID):

        url = str(self.live_server_url) + "/api/"

        try:
            response = req.get(url + "pictures/" + str(emp_ID) + "/")
            response.raise_for_status()
        except req.exceptions.HTTPError as err:
            print(err)

        content = response.json()

        for picture in content:
            for key in picture:
                print(key + ":", picture[key])
            print()
            
        return response

    
    # Retrieve and display a single picture based on a name
    def get_single_picture(self, name):

        url = str(self.live_server_url) + "/api/"

        try:
            response = req.get(url + "pictures/" + name + "/")
            response.raise_for_status()
        except req.exceptions.HTTPError as err:
            print(err)

        picture = response.json()

        for key in picture:
            print(key + ":", picture[key])
        print()
            
        return response
    

    # Update a picture's name
    def update_picture_name(self, old_name, new_name):
        
        url = str(self.live_server_url) + "/api/"
        
        data = {
            "name": new_name,
        }

        try:
            response = req.put(url + "pictures/" + old_name + "/", json=data)
            response.raise_for_status()
        except req.exceptions.HTTPError as err:
            print(err)

        return response
            

    # Delete a picture with a given name
    def delete_picture(self, name):

        url = str(self.live_server_url) + "/api/"

        try:
            response = req.delete(url + "pictures/" + name + "/")
            response.raise_for_status()
        except req.exceptions.HTTPError as err:
            print(err)

        return response
            
            
    # Test all of the Picture API functionalities
    def test_pictures(self):
        
        print()
        
        # Create two employees to add pictures to (emp_ID = 300, 500)
        self.create_employees()
        # Add two pictures to employee 300 and one to employee 500
        self.add_picture(300, MEDIA_ROOT + "TestPics/300_0.jpg")
        self.add_picture(300, MEDIA_ROOT + "TestPics/300_1.jpg")
        self.add_picture(500, MEDIA_ROOT + "TestPics/500_0.jpg")
        self.add_picture(500, MEDIA_ROOT + "TestPics/500_1.jpg")

        # Display all pictures
        print("ALL PICTURES, INITIAL:")
        self.get_pictures()
        print()
        # Display pictures belonging to employee 300
        print("EMPLOYEE 500 PICTURES, INITIAL:")
        self.get_emp_pictures(500)
        print()
        # Display picture 300_0
        print("EMPLOYEE 500 PICTURE 2, INITIAL:")
        self.get_single_picture("500_1")
        print()

        # Change picture 500_1 to 500_2
        self.update_picture_name("500_1", "500_2")
        # Display employee 500 pictures
        print("EMPLOYEE 500 PICTURES, AFTER CHANGING 500_1 TO 500_2:")
        self.get_emp_pictures(500)
        print()

        # Delete employee 300
        Employee.objects.get(emp_ID=300).delete()
        # Display all pictures after deletion
        print("ALL PICTURES, AFTER DELETING EMPLOYEE 300")
        self.get_pictures()
        print()

        # Delete picture 500_2
        self.delete_picture("500_2")
        # Display all pictures after deletion
        print("ALL PICTURES, AFTER DELETING PICTURE 500_2")
        self.get_pictures()
        print()
        
        # Manually delete all Employee objects
        # (This automatically deletes all picture objects)
        Employee.objects.all().delete()
