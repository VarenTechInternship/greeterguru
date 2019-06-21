from django.contrib import admin
from django.contrib.admin import site
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
import django.contrib.auth.admin
from .models import *
from . import views

admin.autodiscover()

#admin.site.register(emp)
admin.site.unregister(Group)
