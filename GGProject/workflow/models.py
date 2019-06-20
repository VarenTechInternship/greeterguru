from django.db import models

#authen = models.BooleanField("Two-factor Authentication?", default=0)

class Employee(models.Model):
    first_name = models.CharField(max_length=30, primary_key = True)
    last_name = models.CharField(max_length=30)
    emp_ID = models.IntegerField(default=0)
    emp_email = models.EmailField(max_length = 254, blank = True)
    keycode = models.PositiveSmallIntegerField(default = 0)
    manager_email = models.EmailField(max_length = 254, default = "")
    
    #configures roles for different types of employees
    permissions_choices = [ 
        (0,'Never'),     # 0 can never unlock door
        (1,'Sometimes'), # 1 can unlock the door given the alarm is off
        (2,'Always'),    # 2 can always unlock the door
    ]
    emp_permissions = models.CharField(
        max_length = 15,
        choices = permissions_choices,
        default = 0
    )

    def __str__(self):
        return("{} {}".format(self.first_name, self.last_name))


class Picture(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    picture = models.ImageField(null=True)
    name = models.CharField(null=True, unique=True, max_length=30)
    
    def __str__(self):
        return("{}".format(self.name))
    

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



    
#Save unknown photos
class Temp_Photo(models.Model):
    temp_id = models.AutoField(max_length = 100, primary_key = True)
    def temp_path(instance, filename):
        return 'temp/{0}'.format(self.temp_id)
    unknown_photo = models.FileField(upload_to = temp_path)
    #sends photos to MEDIA_ROOT set in GreeterGuru/GGProject/GreeterGuru/settings.py
