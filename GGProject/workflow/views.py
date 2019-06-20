from rest_framework import generics
from .models import Employee, Admin, Photo, Temp_Photo
from .serializers import EmployeesSerializer, AdminsSerializer, PhotosSerializer, TempPhotosSerializer

# Displays all Employees' attributes
class ListEmployeesView(generics.ListAPIView):
    # Set of attributes to query
    queryset = Employee.objects.all()
    serializer_class = EmployeesSerializer
class ListAdminsView(generics.ListAPIView):
    # Set of attributes to query
    queryset = Admin.objects.all()
    serializer_class = AdminsSerializer
class ListPhotosView(generics.ListAPIView):
    # Set of attributes to query
    queryset = Photo.objects.all()
    serializer_class = PhotosSerializer
class ListTempPhotosView(generics.ListAPIView):
    # Set of attributes to query
    queryset = Temp_Photo.objects.all()
    serializer_class = TempPhotosSerializer
