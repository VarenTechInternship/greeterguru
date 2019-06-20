from django.contrib import admin
from .models import Employee, Admin, Photo, Temp_Photo
import django.contrib.auth.admin
from django.db import models
from django.contrib.auth.models import *
from django.urls import reverse
# Register your models here.


class AdminsPage(admin.ModelAdmin):
    list_display = ('admin_id', 'admin_email', 'admin_permissions', 'is_two_factor')
    def save_model(self, request, obj, form, change):
        obj.Admin = request.Admin
        super().save_model(request, obj, form, change)
        print(Admin)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'emp_ID', 'emp_email','emp_permissions','manager_email', 'key_code')

    def save_model(self, request, obj, form, change):
        obj.Employee = request.Employee
        super().save_model(request, obj, form, change)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('photo_id', 'badge_photo', 'photos')

    def save_model(self, request, obj, form, change):
        obj.Photo = request.Photo
        super().save_model(request, obj, form, change)
class Temp_PhotoAdmin(admin.ModelAdmin):
    list_display = ('temp_id','unknown_photo')

    def save_model(self, request, obj, form, change):
        obj.Temp_Photo = request.Temp_Photo
        super().save_model(request, obj, form, change)
admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Admin, AdminsPage)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Temp_Photo, Temp_PhotoAdmin)

AdminsPage.save_as = True
EmployeeAdmin.save_as = True
PhotoAdmin.save_as = True
Temp_PhotoAdmin.save_as = True
