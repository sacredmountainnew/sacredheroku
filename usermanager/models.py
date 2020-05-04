from __future__ import unicode_literals
from django.db import models

class UserManager(models.Model):

    name = models.CharField(max_length=30, default="")
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    ip = models.TextField(default="")
    geolocation = models.TextField(default="")

    def __str__(self):

        return self.name