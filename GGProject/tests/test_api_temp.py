from django.test import LiveServerTestCase
from django.core.files import File
from GreeterGuru.settings import MEDIA_ROOT
from workflow.models import TempPhoto
import requests as req
import json


# Requires files temp1.jpg, temp2.jpg, and temp3.jpg
# to be located at GreeterGuru/FaceID/TestPics/
class TempPhotoTests(LiveServerTestCase):

    # Create a temporary photo
    def create_temp_photo(self, pic_name):

        url = str(self.live_server_url) + "/api/"

        files = {"file" : open(pic_name, 'rb')}

        response = req.post(url + "temp-photos/", files=files)
        response.raise_for_status()
        return response.json()

    # Retrieve all temporary photos
    def get_temp_photos(self):

        url = str(self.live_server_url) + "/api/"

        response = req.get(url + "temp-photos/")
        response.raise_for_status()
        return response.json()


    # Delete all temporary photo objects
    def delete_temp_photos(self):

        url = str(self.live_server_url) + "/api/"

        response = req.delete(url + "temp-photos/")
        response.raise_for_status()
        return response


    # Tests all TempPhoto API functionalities
    def test_temp_photos(self):

        # Create three temporary photos
        # After each addition, immediately verify the picture was name correctly
        pic = self.create_temp_photo(MEDIA_ROOT + "/TestPics/temp1.jpg")
        self.assertEqual(pic["name"], "temp1")
        pic = self.create_temp_photo(MEDIA_ROOT + "/TestPics/temp2.jpg")
        self.assertEqual(pic["name"], "temp2")
        pic = self.create_temp_photo(MEDIA_ROOT + "/TestPics/temp3.jpg")
        self.assertEqual(pic["name"], "temp3")

        # Verify all temporary photos were successfully created
        pic_all = self.get_temp_photos()
        self.assertEqual(len(pic_all), 3)

        # Delete all temporary photos
        self.delete_temp_photos()
        # Verify all temporary photos were successfully created
        pic_all = self.get_temp_photos()
        self.assertEqual(len(pic_all), 0)

        # Manually delete all TempPhoto objects
        TempPhoto.objects.all().delete()
