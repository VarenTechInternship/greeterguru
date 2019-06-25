from django.contrib import admin
from .models import Employee, Picture, TempPhoto
import django.contrib.auth.admin
from django.db import models
from django.contrib.auth.models import *
from django.urls import reverse

# Register your models here.
admin.site.unregister(Group)
#admin.site.unregister(User)

admin.site.register(Employee)
admin.site.register(Picture)
admin.site.register(TempPhoto)
