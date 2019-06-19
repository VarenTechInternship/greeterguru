from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee, Picture
from .serializers import EmployeesSerializer, PicturesSerializer


# API for handling all employees
@api_view(['GET', 'POST'])
def ListEmployees(request):

    # Return all employee information
    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeesSerializer(employees, many=True)
        return Response(serializer.data)

    # Add new employee to database
    elif request.method == 'POST':
        serializer = EmployeesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    
# API for handling a single employee based on their employee ID
@api_view(['GET', 'PUT', 'DELETE'])
def SingleEmployee(request, emp_ID):

    # Retrieve employee according to passed employee ID
    try:
        employee = Employee.objects.get(emp_ID=emp_ID)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Return retrieved employee
    if request.method == 'GET':
        serializer = EmployeesSerializer(employee)
        return Response(serializer.data)

    # Update the retrieved employee
    elif request.method == 'PUT':
        serializer = EmployeesSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # Delete retrieved employee
    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

# API for handling all pictures    
@api_view(['GET'])
def ListPictures(request):

    # Return all pictures
    if request.method == 'GET':
        pictures = Picture.objects.all()
        serializer = PicturesSerializer(pictures, many=True)
        return Response(serializer.data)

    
# API for handling pictures based on employee ID of the employee they belong to
@api_view(['GET', 'POST'])
def EmployeePictures(request, emp_ID):

    # Retrieve employee based on passed employee ID
    try:
        employee = Employee.objects.get(emp_ID=emp_ID)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Retrieve all pictures belonging to that employee
    pictures = Picture.objects.all().filter(employee=employee)

    # Return retrieved pictures
    if request.method == 'GET':
        serializer = PicturesSerializer(pictures, many=True)
        return Response(serializer.data)

    # Create new picture belonging to retrieved employee
    elif request.method == 'POST':
        serializer = PicturesSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.validated_data["employee"] = employee
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# API for handling a single picture based on its name   
@api_view(['GET', 'PUT', 'DELETE'])
def SinglePicture(request, name):

    # Retrieve picture based on based name
    try:
        picture = Picture.objects.get(name=name)
    except Picture.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Return retrieved picture
    if request.method == 'GET':
        serializer = PicturesSerializer(picture)
        return Response(serializer.data)

    # Update retrieved picture
    elif request.method == 'PUT':
        serializer = PicturesSerializer(picture, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete retrieved picture
    elif request.method == 'DELETE':
        picture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
