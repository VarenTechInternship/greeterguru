from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.ListEmployees, name="employees-all"),
    path('employees/<int:varen_ID>', views.SingleEmployee, name="employees-one"),
    path('pictures/', views.ListPictures, name="pictures-all"),
    path('pictures/<int:varen_ID>', views.EmployeePictures, name="pictures-one"),
]
