from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.models import User, Group

def send(request):
    emp1 = User(username = 'orndorffc',first_name = "caroline", last_name = "orndorff", email = "orndorffc@varentech.com")
    emp1.save()
    name = emp1.get_full_name(self)
    print(name)
    return render(request)
