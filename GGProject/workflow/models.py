from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Employee class acting as a custom User class
class Employee(AbstractUser):

    # Information about the entire class
    class Meta:
        verbose_name = "Employee"

    """
    Built in User attributes:
     - username (required): login name, formatted as last name + first initial
     - password (required): login password, hashed
     - is_active: is the user still active?
     - is_staff: is the user allowed to access the site?
     - is_superuser: is the user an admin?
     - first_name: first name
     - last_name: last name
     - email: valid email address
    """

    # Whether the user is still active
    is_active = models.BooleanField(
        default = True,
        verbose_name = "Active",
        help_text = "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
    )

    # Whether the user can access the site
    is_staff = models.BooleanField(
        default = False,
        verbose_name = "Staff status",
        help_text = "Designates whether the user can log into this admin site."
    )

    # Employee's company email address
    email = models.EmailField(
        null = True,
        blank = True,
        verbose_name = "Company email",
        help_text = "Company email address in the format email@example.com."
    )

    # Employee's ID number that must be unique
    emp_ID = models.PositiveSmallIntegerField(
        unique = True,
        null = True,
        blank = True,
        verbose_name = "Employee ID",
        help_text = "Unique integer identifier."
    )

    # Employee's keycode number
    keycode = models.PositiveSmallIntegerField(
        null = True,
        blank = True,
        default = 0,
        help_text = "Five digit code for accessing building."
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
        null = True,
        blank = True,
        verbose_name = "Access level",
        help_text = "Designates when the employee is allowed to access the building."
    )

    # True if user only exists in web database
    database_only = models.BooleanField(
        default = False,
        verbose_name = "Database only",
        help_text = "Designates whether the user exists only in the web database and not in the active directory. If false while the user is not in active directory, they will be deleted during next database update."
    )

    # Display Employees as "username (emp_ID)"
    def __str__(self):
        return("{} ({})".format(self.username, self.emp_ID))


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
        upload_to = "dataset/",
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

    # Information about the entire class
    class Meta:
        verbose_name = "Unknown Photo"

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


# Automatically make every superuser database only
@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def make_database_only(sender, instance=None, created=False, **kwargs):
    if instance.is_superuser:
        instance.database_only = True


# Automatically generate authentication token for every user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
