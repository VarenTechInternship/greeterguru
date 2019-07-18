from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Employee class acting as a custom User class
class Employee(AbstractUser):

    """
    Built in User attributes:
     - username (required): login name, formatted as last name + first initial
     - password (required): login password, hashed
     - is_superuser: is the user/employee an admin?
     - is_staff: is the user/employee allowed to access the site?
     - first_name: first name
     - last_name: last name
     - email: valid email address
    """

    email = models.EmailField(
        null = True,
        verbose_name = "Company email",
        help_text = "Company email address in the format example@email.com."
    )

    # Employee's ID number that must be unique
    emp_ID = models.PositiveSmallIntegerField(
        null = True,
        unique = True,
        verbose_name = "Employee ID",
        help_text = "Required. Unique integer identifier."
    )

    # Employee's keycode number
    keycode = models.PositiveSmallIntegerField(
        null = True,
        default = 0,
        help_text = "Five digit code for accessing building. Used for two-factor authentication."
    )

    # Available roles for different types of employees
    PERMISSIONS_CHOICES = (
        ('0', 'Never'),     # 0 can never unlock door
        ('1', 'Sometimes'), # 1 can unlock the door given the alarm is off
        ('2', 'Always'),    # 2 can always unlock the door
    )
    # Employee's access permission level
    permissions = models.CharField(
        max_length = 15,
        choices = PERMISSIONS_CHOICES,
        default = 0,
        verbose_name = "Employee permissions",
        help_text = "Designates when the employee is allowed to access the building."
    )


# Pictures that belong to an employee
class Picture(models.Model):

    # Employee that the picture belongs to
    employee = models.ForeignKey(
        Employee,
        on_delete = models.CASCADE,
        null = True
    )

    # Actual image file, stored in GreeterGuru/FaceID/Dataset
    picture = models.ImageField(
        upload_to = "Dataset/",
        null = True
    )

    # Shorthand name of the picture
    name = models.CharField(
        null = True,
        unique = True,
        max_length = 30
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
        verbose_name ="Temporary ID"
    )

    # Actual image file, stored in GreeterGuru/FaceID/TempPhotos
    unknown_photo = models.ImageField(
        upload_to = "TempPhotos/",
        null = True
    )

    # Shorthand name of the picture
    name = models.CharField(
        null = True,
        unique = True,
        max_length = 30
    )

    # Printing a temporary photo outputs its shorthand name
    def __str__(self):
        return("{}".format(self.name))


# Automatically generate authentication token for every user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
