from django.db import models

#authen = models.BooleanField("Two-factor Authentication?", default=0)

# Create your models here.
class Employee(models.Model):
    #includes first_name, last_name, emp_ID, emp_email, emp_permissions, manager_email, key_code
    first_name = models.CharField(max_length=30, primary_key = True)
    last_name = models.CharField(max_length=30)
    emp_ID = models.IntegerField(default=0)

    def __str__(self):
        return("{} {}".format(self.first_name, self.last_name))

    emp_email = models.EmailField(max_length = 254, default = "")
    permissions_choices = [ #configures roles for different types of employees
        # 0 can never unlock door
        # 1 can unlock the door given the alarm is off
        # 2 can always unlock the door
        (0,'Never'),
        (1,'Sometimes'),
        (2,'Always'),
    ]
    emp_permissions = models.CharField(
        max_length = 15,
        choices = permissions_choices,
        default = 0
    )
    #Manager Information
    manager_email = models.EmailField(max_length = 254, default = "")
    #used only for two-factor authentication
    key_code = models.PositiveSmallIntegerField(default = 0)

#class Admin(models.Model):
class Admin(models.Model):
    #includes admin_id, admin_email, admin_permissions, is_two_factor
    admin_id = models.IntegerField(primary_key = True)
    admin_email = models.EmailField(max_length = 254, default = "")
    admin_permissions_choices = [
        (0,'User'),
        (1,'Superuser'),
        (2,'Superadmin'),
    ]
    admin_permissions = models.CharField(
        max_length = 15,
        choices = admin_permissions_choices,
        default = 0
    )
    is_two_factor = models.BooleanField("Two-Factor Authentication", default = False)

#Save recognized photos
class Photo(models.Model):
    photo_id = models.ForeignKey(Employee, on_delete = models.CASCADE, related_name = "+")
    badge_photo = models.ImageField()
    #sets name of photo file
    def user_directory_path(instance, filename):
        return 'user_{0}/{1}'.format(instance.Employee.emp_ID, photo_id)
    photos = models.FileField(upload_to = user_directory_path)
    #sends photos to MEDIA_ROOT set in GreeterGuru/GGProject/GreeterGuru/settings.py

#Save unknown photos
class Temp_Photo(models.Model):
    temp_id = models.AutoField(max_length = 100, primary_key = True)
    def temp_path(instance, filename):
        return 'temp/{0}'.format(self.temp_id)
    unknown_photo = models.FileField(upload_to = temp_path)
    #sends photos to MEDIA_ROOT set in GreeterGuru/GGProject/GreeterGuru/settings.py
