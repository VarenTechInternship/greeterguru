# Add url paths for workflow app
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.views import login

from workflow.views import updateAD
from workflow.admin import admin_site

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^admin_tools/', include('admin_tools.urls')),
]
