from django.db import models

# Employee
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


# Store pictures that belong to an employee
class Picture(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    picture = models.ImageField(upload_to="Dataset/", null=True)
    name = models.CharField(null=True, unique=True, max_length=30)
    
    def __str__(self):
        return("{}".format(self.name))


# Save unknown photos
class Temp_Photo(models.Model):
    temp_id = models.AutoField(max_length = 100, primary_key = True)
    picture = models.ImageField(upload_to="Temp Photos/", null=True)
    name = models.CharField(null=True, unique=True, max_length=30)
    
    def __str__(self):
        return("{}".format(self.name))    
