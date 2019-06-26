# Add url paths for workflow app
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.views import login
from django.urls import path
from . import views
import rest_framework

admin.autodiscover()

urlpatterns = [
    path('employees/', views.ListEmployees.as_view()),
    path('employees/<int:emp_ID>/', views.SingleEmployee.as_view()),
    path('pictures/', views.ListPictures.as_view()),
    path('pictures/<int:emp_ID>/', views.EmployeePictures.as_view()),
    path('pictures/<str:name>/', views.SinglePicture.as_view()),
    path('temp-photos/', views.ListTempPhotos.as_view()),
    path('token-auth/', rest_framework.authtoken.views.obtain_auth_token),
]
