from django.contrib import admin
from .models import Employee, Admin, Photo, Temp_Photo
import django.contrib.auth.admin
from django.db import models
from django.contrib.auth.models import *
from django.urls import reverse

# Register your models here.
admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.register(Employee)
admin.site.register(Admin)
admin.site.register(Photo)
admin.site.register(Temp_Photo)
