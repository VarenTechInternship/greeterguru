from django.db import models

# Create your models here.
class emp (models.Model):
    first=models.CharField(null = True, max_length = 10)
    last=models.CharField(null=True, max_length = 10)
