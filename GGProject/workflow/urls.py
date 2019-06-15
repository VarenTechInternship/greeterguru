from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.ListEmployeesView.as_view(), name="employees-all"),
]

