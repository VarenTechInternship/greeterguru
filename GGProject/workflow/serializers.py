from rest_framework import serializers
from .models import Employee

# Serializer for the employee class
class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("first_name", "last_name", "emp_ID", "emp_email","emp_permissions","manager_email", "key_code")

# Serializer for the employee class
#class EmployeesSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Employee
#        fields = ("first_name", "last_name", "primary_key", "authen")
