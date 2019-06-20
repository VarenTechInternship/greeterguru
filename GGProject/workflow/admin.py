from django.contrib import admin
from django.contrib.auth.models import User, Group

from django.db import models
import django.contrib.auth.admin
from .models import *

admin.autodiscover()

admin.site.register(emp)
admin.site.unregister(User)
admin.site.unregister(Group)
