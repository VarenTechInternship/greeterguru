from django.db import models

# Create your models here.
class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    primary_key = models.IntegerField(default=0)
    authen = models.BooleanField("Two-factor Authentication?", default=0)

    def __str__(self):
        return("{} {}".format(self.first_name, self.last_name))
