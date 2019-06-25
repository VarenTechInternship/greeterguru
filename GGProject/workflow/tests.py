from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Employee
from .serializers import EmployeesSerializer
from . import views


# Place your tests here
