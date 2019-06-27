from django.test import LiveServerTestCase
from django.core.files import File
from GreeterGuru.settings import MEDIA_ROOT
from workflow.models import TempPhoto
import requests, json


# Requires files temp1.jpg, temp2.jpg, and temp3.jpg
# to be located at GreeterGuru/FaceID/TestPics/
class TempPhotoTests(LiveServerTestCase):

    # Create a temporary photo
    def create_temp_photo(self, pic_name):

        url = str(self.live_server_url) + "/api/"

        files = {"file" : open(pic_name, 'rb')}

        try:
            response = requests.post(url + "temp-photos/", files=files)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)

        return response


    # Retrieve and display all temporary photos
    def get_temp_photos(self):

        url = str(self.live_server_url) + "/api/"

        try:
            response = requests.get(url + "temp-photos/")
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)

        content = response.json()

        for photo in content:
            for key in photo:
                print(key + ":", photo[key])
            print()
            
        return response
    

    # Delete all temporary photo objects
    def delete_temp_photos(self):

        url = str(self.live_server_url) + "/api/"
        
        try:
            response = requests.delete(url + "temp-photos/")
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
    
        return response

            
    # Tests all TempPhoto API functionalities            
    def test_temp_photos(self):

        print()
        
        # Create three temporary photos
        self.create_temp_photo(MEDIA_ROOT + "/TestPics/temp1.jpg")
        self.create_temp_photo(MEDIA_ROOT + "/TestPics/temp2.jpg")
        self.create_temp_photo(MEDIA_ROOT + "/TestPics/temp3.jpg")

        # Display all temporary photos
        print("ALL TEMPORARY PHOTOS, INITIAL:")
        self.get_temp_photos()
        print()

        # Delete all temporary photos
        self.delete_temp_photos()
        # Confirm they were deleted
        if TempPhoto.DoesNotExist:
            print("ALL TEMP PHOTOS SUCCESSFULLY DELETED")
        else:
            print("DELETION OF ALL TEMP PHOTOS FAILED")
            
        # Manually delete all TempPhoto objects
        TempPhoto.objects.all().delete()
