# Add url paths for workflow app
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.views import login
from django.urls import path
from . import views

admin.autodiscover()

urlpatterns = [
    path('employees/', views.ListEmployeesView.as_view(), name="employees-all"),
    path('pictures/', views.ListPicturesView.as_view(), name="pictures-all"),
    path('temp-photos/', views.ListTempPhotosView.as_view(), name="temp-photos-all"),

]
