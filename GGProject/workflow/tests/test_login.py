from django.test import TestCase, Client
import unittest


class TestCase(TestCase):
    def test_details(self):
        self.client = Client()
        response = self.client.post('/login/', {'username':'root', 'password':'GreeterGuru'})
        print(response.status_code)

    
