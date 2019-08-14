from rest_framework import serializers
from workflow.models import Employee, Picture


# Serializer for the Employee class
class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "username",
            "is_superuser",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "email",
            "emp_ID",
            "keycode",
            "permissions",
            "database_only",
        )

# Serializer for the Picture class
class PicturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = (
            'employee',
            'picture',
            'name',
        )
