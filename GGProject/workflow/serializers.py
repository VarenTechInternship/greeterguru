from rest_framework import serializers
from .models import Employee, Admin, Photo, Temp_Photo

# Serializer for the employee class
class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("first_name", "last_name", "emp_ID", "emp_email","emp_permissions","manager_email", "key_code")
class AdminsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ('admin_id', 'admin_email', 'admin_permissions', 'is_two_factor')
class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('photo_id', 'badge_photo', 'photos')
class TempPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temp_Photo
        fields = ('temp_id','unknown_photo')
# Serializer for the employee class
#class EmployeesSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Employee
#        fields = ("first_name", "last_name", "primary_key", "authen")
