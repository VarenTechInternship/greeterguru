from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.ListEmployeesView.as_view(), name="employees-all"),
    #path('employees/<int:pk>/', views.SingleEmployeeView, name="employee-one"),
    path('admin/', views.ListAdminsView.as_view(), name="admins-all"),
    path('photo/', views.ListPhotosView.as_view(), name="photos-all"),
    path('temp-photo/', views.ListTempPhotosView.as_view(), name="temp-photos-all"),

]
