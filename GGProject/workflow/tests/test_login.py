from django.test import TestCase, Client, LiveServerTestCase
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from workflow import admin
from django.conf.urls import url
from django.urls import reverse
import requests as request

class LoginTest(LiveServerTestCase):
    def test_login(self):
        #create super User
        test_admin = User.objects.create_superuser('root','','GreeterGuru')
        url = str(self.live_server_url) + "/login/"
        self.client = Client()
        session = request.Session()
        r = session.get(url)
        User.objects.all()
        user = authenticate(username = 'root', password = 'GreeterGuru')
        user.is_active == True
        self.client.login()
        #self.client.login(username = test_admin.username, password = test_admin.password)

        try:
            response = request.Session().post(str(self.live_server_url))
            #response = requests.get(str(self.live_server_url))
            response.raise_for_status()
        except request.exceptions.HTTPError as err:
            print(err)
        return response
