from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
import django.contrib.auth.admin
from .models import *
from . import views

from .models import Employee, Picture
admin.autodiscover()

#admin.site.register(emp)
admin.site.unregister(Group)
admin.site.unregister(User)

# Register your models here.
admin.site.register(Employee)
admin.site.register(Picture)
