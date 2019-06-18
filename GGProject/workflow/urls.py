from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.ListEmployees, name="employees-all"),
    path('employees/<int:pk>/', views.SingleEmployee, name="employees-one"),
    path('pictures/', views.ListPictures, name="pictures-all"),
    path('pictures/<int:pk>/', views.SinglePicture, name="pictures-one"),
]
