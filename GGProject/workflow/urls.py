from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.ListEmployees),
    path('employees/<int:emp_ID>/', views.SingleEmployee),
    path('pictures/', views.ListPictures),
    path('pictures/<int:emp_ID>/', views.EmployeePictures),
    path('pictures/<str:name>/', views.SinglePicture),
]
