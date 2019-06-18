from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from .models import Employee, Picture
from .serializers import EmployeesSerializer, PicturesSerializer

# API for handling all employees
@api_view(['GET', 'POST'])
def ListEmployees(request):

    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeesSerializer(employees, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = EmployeesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=statis.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    
# API for handling a single employee based on their primary key
@api_view(['GET', 'POST', 'DELETE'])
def SingleEmployee(request, pk):

    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmployeesSerializer(employee)
        return Response(serializer.data)

    
# API for handling all pictures    
@api_view(['GET'])
def ListPictures(request):

    if request.method == 'GET':
        pictures = Picture.objects.all()
        serializer = PicturesSerializer(pictures, many=True)
        return Response(serializer.data)

    
# API for handling pictures based on primary key of the employee they belong to
@api_view(['GET', 'POST', 'DELETE'])
def SinglePicture(request, pk):
    
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    pictures = Picture.objects.all().filter(employee=employee)
    
    if request.method == 'GET':
        serializer = PicturesSerializer(pictures, many=True)
        return Response(serializer.data)

    #if request.method == 'POST':
        # Deter
