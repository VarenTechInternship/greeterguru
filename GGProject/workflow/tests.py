from django.test import TestCase
<<<<<<< HEAD

# Create your tests here.
=======
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Employee
from .serializers import EmployeesSerializer
from . import views


# Place your tests here
>>>>>>> 33334a727aab38b2014962cb1609515e70ddc8b9
