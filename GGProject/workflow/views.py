from django.http import Http404, HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Employee, Picture, TempPhoto
from .serializers import EmployeesSerializer, PicturesSerializer, TempPhotosSerializer
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.models import User

# Allows access to anyone - Use for development
authen = (AllowAny,)
# Only allows access to authenticated admins - Use for final implementation
#authen = (IsAdminUser,)


# API for handling all employees
class ListEmployees(APIView):

    permission_classes = authen

    # Return all employee information
    def get(self, request, format=None):
        employees = Employee.objects.all()
        serializer = EmployeesSerializer(employees, many=True)
        return Response(serializer.data)

    # Add new employee to database
    def post(self, request, format=None):
        serializer = EmployeesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# API for handling a single employee based on their employee ID
class SingleEmployee(APIView):

    permission_classes = authen

    # Retrieve employee according to passed employee ID
    def get_employee(self, emp_ID):
        try:
            return Employee.objects.get(emp_ID=emp_ID)
        except Employee.DoesNotExist:
            raise Http404

    # Return retrieved employee
    def get(self, request, emp_ID, format=None):
        employee = self.get_employee(emp_ID)
        serializer = EmployeesSerializer(employee)
        return Response(serializer.data)

    # Update the retrieved employee
    def put(self, request, emp_ID, format=None):
        employee = self.get_employee(emp_ID)
        serializer = EmployeesSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete retrieved employee
    def delete(self, request, emp_ID, format=None):
        employee = self.get_employee(emp_ID)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# API for handling all pictures
class ListPictures(APIView):

    permission_classes = authen

    # Retrieve all pictures
    def get(self, request):
        pictures = Picture.objects.all()
        serializer = PicturesSerializer(pictures, many=True)
        return Response(serializer.data)


# API for handling pictures based on employee ID of the employee they belong to
class EmployeePictures(APIView):

    permission_classes = authen

    # Retrieve employee according to passed employee ID
    def get_employee(self, emp_ID):
        try:
            return Employee.objects.get(emp_ID=emp_ID)
        except Employee.DoesNotExist:
            raise Http404

    # Return retrieved pictures
    def get(self, request, emp_ID):
        employee = self.get_employee(emp_ID)
        pictures = Picture.objects.all().filter(employee=employee)
        serializer = PicturesSerializer(pictures, many=True)
        return Response(serializer.data)

    # Create new picture belonging to retrieved employee
    def post(self, request, emp_ID):
        employee = self.get_employee(emp_ID)
        serializer = PicturesSerializer(data={})
        if serializer.is_valid():
            # Add all necessary attributes
            serializer.validated_data["employee"] = employee
            serializer.validated_data["picture"] = request.FILES['file']
            pic_name = request.FILES['file'].name.split(".")[0]
            serializer.validated_data["name"] = pic_name
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API for handling a single picture based on its name
class SinglePicture(APIView):

    permission_classes = authen

    # Retrieve picture according to passed name
    def get_picture(self, name):
        try:
            return Picture.objects.get(name=name)
        except Picture.DoesNotExist:
            raise Http404

    # Return picture information
    def get(self, request, name):
        picture = self.get_picture(name)
        serializer = PicturesSerializer(picture)
        return Response(serializer.data)

    # Update picture
    def put(self, request, name):
        picture = self.get_picture(name)
        serializer = PicturesSerializer(picture, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete retrieved picture
    def delete(self, request, name):
        picture = self.get_picture(name)
        picture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# API for handling all temporary photos
class ListTempPhotos(APIView):

    permission_classes = authen

    # Return all temporary photos
    def get(self, request):
        tempPhotos = TempPhoto.objects.all()
        serializer = TempPhotosSerializer(tempPhotos, many=True)
        return Response(serializer.data)

    # Create and add new temporary photo
    def post(self, request):
        serializer = TempPhotosSerializer(data={})
        if serializer.is_valid():
            # Add all necessary attributes
            serializer.validated_data["unknown_photo"] = request.FILES['file']
            pic_name = request.FILES['file'].name.split(".")[0]
            serializer.validated_data["name"] = pic_name
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete all temporary photos
    def delete(self, request):
        TempPhoto.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateAD(View):
    def get(self, request):
        return render(request, "update_ad.html")

class AuthFactor(View):
    def get(self, request):
        return render(request, "auth_options.html")
