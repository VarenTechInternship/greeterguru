from django.urls import path
from . import views


urlpatterns = [
    path('ad/', views.UpdateAD.as_view(), name = 'updatead'),
    path('authfactor/', views.AuthFactor.as_view(), name = 'authfactor'),
]
