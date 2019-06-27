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
    def test_workflow(self):
        client = Client()
        response = client.get('/workflow/')
        self.assertEqual(response.status_code, 302)
    def test_employee(self):
        client = Client()
        response = client.get('/workflow/employee/')
        self.assertEqual(response.status_code, 302)
    def test_employee_add(self):
        client = Client()
        response = client.get('/workflow/employee/add/')
        self.assertEqual(response.status_code, 302)
    def test_picture(self):
        client = Client()
        response = client.get('/workflow/picture/')
        self.assertEqual(response.status_code, 302)
    def test_picture_add(self):
        client = Client()
        response = client.get('/workflow/picture/add/')
        self.assertEqual(response.status_code, 302)
