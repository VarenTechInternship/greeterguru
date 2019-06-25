from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader

from rest_framework import generics
from .models import Employee, Picture, TempPhoto
from .serializers import EmployeesSerializer, PicturesSerializer, TempPhotosSerializer

# Displays all Employees' attributes
class ListEmployeesView(generics.ListAPIView):
    # Set of attributes to query
    queryset = Employee.objects.all()
    serializer_class = EmployeesSerializer

# Displays all Pictures' attributes
class ListPicturesView(generics.ListAPIView):
    # Set of attributes to query
    queryset = Picture.objects.all()
    serializer_class = PicturesSerializer

# Displays all TempPhotos' attributes
class ListTempPhotosView(generics.ListAPIView):
    # Set of attributes to query
    queryset = TempPhoto.objects.all()
    serializer_class = TempPhotosSerializer
