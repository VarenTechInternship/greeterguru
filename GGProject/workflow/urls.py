from django.urls import path
from . import views
import rest_framework
from rest_framework.authtoken import views as authviews

urlpatterns = [
    path('employees/', views.ListEmployees.as_view()),
    path('employees/<int:emp_ID>/', views.SingleEmployee.as_view()),
    path('pictures/', views.ListPictures.as_view()),
    path('pictures/<int:emp_ID>/', views.EmployeePictures.as_view()),
    path('pictures/<str:name>/', views.SinglePicture.as_view()),
    path('temp-photos/', views.ListTempPhotos.as_view()),
    path('token-auth/', rest_framework.authtoken.views.obtain_auth_token),
]
