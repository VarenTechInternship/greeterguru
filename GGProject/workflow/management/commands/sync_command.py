import requests as req
import ldap
from django_auth_ldap.backend import LDAPBackend
from django.core.management.base import BaseCommand, CommandError
from GreeterGuru import settings
from scripts import adminOptions

class Command(BaseCommand):

    help = "Synchronizes web database employees with active directory users"
    
    def handle(self, *args, **kwargs):

        adminOptions.populate()
