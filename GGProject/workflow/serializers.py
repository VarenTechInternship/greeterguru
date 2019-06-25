from rest_framework import serializers

from .models import Employee, Picture, TempPhoto

# Serializer for the employee class
class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("first_name", "last_name", "emp_ID", "emp_email",
                  "manager_email", "keycode", "emp_permissions", "last_login")

# Serializer for the picture class
class PicturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('employee', 'picture', 'name')

# Serializer for the temporary photo class
class TempPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempPhoto
        fields = ('temp_id','unknown_photo', 'name')
