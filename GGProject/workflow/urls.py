from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.ListEmployeesView.as_view(), name="employees-all"),
    path('pictures/', views.ListPicturesView.as_view(), name="pictures-all"),
    path('temp-photos/', views.ListTempPhotosView.as_view(), name="temp-photos-all"),

]
