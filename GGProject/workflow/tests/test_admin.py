from django.test import TestCase, Client
import unittest
import requests
from django.contrib.auth.models import User
#test pages exist
class TestAdmin(unittest.TestCase):
    client = Client()

    def test_admin(self): #admin main exists
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
    
