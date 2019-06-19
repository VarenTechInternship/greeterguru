from django.contrib import admin
from .models import Employee, Admin, Photo, Temp_Photo
import django.contrib.auth.admin
from django.contrib.auth.models import *

# Register your models here.
admin.site.register(Employee)
admin.site.register(Admin)
admin.site.register(Photo)
admin.site.register(Temp_Photo)

admin.site.unregister(Group)
admin.site.unregister(User)
