"""GreeterGuru URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include, re_path
=======
from django.urls import path, include
>>>>>>> 2d7eba7... Add Django-Admin-Tools
from django.conf.urls import url
from django.contrib.auth.views import login
admin.autodiscover()

urlpatterns = [
<<<<<<< HEAD
    path('', admin.site.urls),
    url(r'^admin_tools/', include('admin_tools.urls')),
    re_path('api/', include('workflow.urls')),
=======
    path('admin/', admin.site.urls),
    url(r'^admin_tools/', include('admin_tools.urls')),
>>>>>>> 2d7eba7... Add Django-Admin-Tools
]
