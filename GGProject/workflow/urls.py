# Add url paths for workflow app
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.views import login

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^admin_tools/', include('admin_tools.urls')),
]
