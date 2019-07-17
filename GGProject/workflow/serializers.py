from rest_framework import serializers
from .models import Employee, Picture, TempPhoto


# Serializer for the Employee class
class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "username",
            "password",
            "is_superuser",
            "is_staff",
            "first_name",
            "last_name",
            "email",
            "emp_ID",
            "keycode",
            "permissions",
        )

# Serializer for the picture class
class PicturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = (
            'employee',
            'picture',
            'name'
        )

# Serializer for the temporary photo class
class TempPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempPhoto
        fields = (
            'temp_id',
            'unknown_photo',
            'name'
        )
