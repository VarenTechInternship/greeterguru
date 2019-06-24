from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
import django.contrib.auth.admin
from .models import *
from . import views
from workflow.views import updateAD
admin.autodiscover()

#admin.site.register(emp)
admin.site.unregister(Group)

class site(AdminSite):
    def get_urls(self):
        from django.conf.urls import url
        urls = super(site, self).get_urls()
        urls = [
            url(r'^AD/$', self.views(updateAD))
        ] + urls
        return urls
admin_site = site()

#admin_site.register()
