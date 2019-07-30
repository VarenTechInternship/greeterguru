from django.http import Http404, HttpResponse
from rest_framework import status
from django.views.generic import View
from rest_framework.permissions import IsAdminUser, AllowAny
from django.views.generic import View
from django.shortcuts import render
from scripts import adminOptions


# View for synchronizing web database with active directory
class UpdateAD(View):
    
    def get(self, request):
        if request.user.is_superuser:
            return render(request, "update_ad.html")
        return HttpResponse(status=405)

    def post(self, request):
        adminOptions.populate()
        return HttpResponse(status=status.HTTP_202_ACCEPTED)


# View for the admin option to set the authentication level
class AuthFactor(View):

    def get(self, request):
        return render(request, "auth_options.html")
