from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from workflow.models import Employee, Picture
from .serializers import EmployeesSerializer, PicturesSerializer
from django.contrib.auth.models import User


# Only allows access to authenticated admins - Use for final implementation
authen = (IsAdminUser,)


# API for handling all employees
class ListEmployees(APIView):

    permission_classes = authen

    # Return all employee information
    def get(self, request, format=None):
        employees = Employee.objects.all()
        serializer = EmployeesSerializer(employees, many=True)
        return Response(serializer.data)


# API for handling a single employee based on their employee ID
class SingleEmployeeID(APIView):

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


# API for handling a single employee based on their username
class SingleEmployeeName(APIView):

    permission_classes = authen

    # Retrieve employee according to passed employee ID
    def get_employee(self, username):
        try:
            return Employee.objects.get(username=username)
        except Employee.DoesNotExist:
            raise Http404

    # Return retrieved employee
    def get(self, request, username, format=None):
        employee = self.get_employee(username)
        serializer = EmployeesSerializer(employee)
        return Response(serializer.data)

    # Delete retrieved employee
    def delete(self, request, username, format=None):
        employee = self.get_employee(username)
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

    # Delete retrieved picture
    def delete(self, request, name):
        picture = self.get_picture(name)
        picture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
