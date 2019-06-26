<<<<<<< HEAD
from django.test import TestCase, Client, LiveServerTestCase
import unittest
from django.conf.urls import url
from django.urls import reverse
from workflow import views
from workflow.models import Employee, Picture, TempPhoto
import requests

#Tests Views
class EmployeeViewsTestCase(TestCase):
    pass
=======
from django.test import TestCase
import unittest
>>>>>>> Create tests directory for app workflow. Create test files for admin, forms, models, views
