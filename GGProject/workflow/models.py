from django.db import models

# Registered employee
class Employee(models.Model):

    # First name of the employee
    first_name = models.CharField(
        null=True,
        max_length=30
    )

    # Last name of the employee
    last_name = models.CharField(
        null=True,
        max_length=30
    )

    # Employee's ID number that must be unique
    emp_ID = models.IntegerField(
        null=True,
        unique=True,
        verbose_name="Employee ID"
    )

    # Employee's email
    emp_email = models.EmailField(
        null=True,
        max_length = 254,
        verbose_name="Employee email"
    )

    # Employee's manager's email
    manager_email = models.EmailField(
        null=True,
        max_length = 254
    )

    # Employee's keycode number
    keycode = models.PositiveSmallIntegerField(
        null=True,
        default = 0
    )
    
    # Available roles for different types of employees
    PERMISSIONS_CHOICES = ( 
        ('0', 'Never'),     # 0 can never unlock door
        ('1', 'Sometimes'), # 1 can unlock the door given the alarm is off
        ('2', 'Always'),    # 2 can always unlock the door
    )
    # Employee's access permission level
    emp_permissions = models.CharField(
        max_length = 15,
        choices = PERMISSIONS_CHOICES,
        default = 0,
        verbose_name="Employee permissions"
    )

    # Date of the last time the employee logged in
    login_time = models.DateField(
        null=True,
        verbose_name="Last login date"
    )

    # Printing an employee outputs their first and last name
    def __str__(self):
        return("{} {}".format(self.first_name, self.last_name))


    
# Pictures that belong to an employee
class Picture(models.Model):

    # Employee that the picture belongs to
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        null=True
    )
    
    # Actual image file, stored in GreeterGuru/FaceID/Dataset
    picture = models.ImageField(
        upload_to="Dataset/",
        null=True
    )

    # Shorthand name of the picture
    name = models.CharField(
        null=True,
        unique=True,
        max_length=30
    )

    # Printing a picture outputs its shorthand name
    def __str__(self):
        return("{}".format(self.name))


    
# Photos belonging to unknown individuals
class TempPhoto(models.Model):

    # Temporary ID for a stored photo
    temp_id = models.AutoField(
        max_length = 100,
        primary_key = True,
        verbose_name="Temporary ID"
    )

    # Actual image file, stored in GreeterGuru/FaceID/TempPhotos
    unknown_photo = models.ImageField(
        upload_to="TempPhotos/",
        null=True
    )

    # Shorthand name of the picture
    name = models.CharField(
        null=True,
        unique=True,
        max_length=30
    )

    # Printing a temporary photo outputs its shorthand name
    def __str__(self):
        return("{}".format(self.name))
