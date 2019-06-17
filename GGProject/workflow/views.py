from rest_framework import generics
from .models import Employee
from .serializers import EmployeesSerializer

# Displays all Employees' attributes
class ListEmployeesView(generics.ListAPIView):
    
    # Set of attributes to query
    queryset = Employee.objects.all()
    serializer_class = EmployeesSerializer
