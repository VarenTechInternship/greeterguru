# Add url paths for workflow app
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.views import login
from django.urls import path
from . import views

admin.autodiscover()

urlpatterns = [
    path('employees/', views.ListEmployees),
    path('employees/<int:emp_ID>/', views.SingleEmployee),
    path('pictures/', views.ListPictures),
    path('pictures/<int:emp_ID>/', views.EmployeePictures),
    path('pictures/<str:name>/', views.SinglePicture),
]
