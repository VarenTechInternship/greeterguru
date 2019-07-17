from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Picture, TempPhoto, Token
from .forms import EmployeeCreationForm


# Defines admin view for Employee model
class EmployeeAdmin(UserAdmin):
    add_form = EmployeeCreationForm
    model = Employee
    list_display = ['username', 'first_name', 'last_name', 'emp_ID']

# Unregister default models
admin.site.unregister(Group)
admin.site.unregister(Token)

# Register create models
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Picture)
admin.site.register(TempPhoto)
