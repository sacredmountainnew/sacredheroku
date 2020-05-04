from __future__ import unicode_literals
from django.db import models

class NewsLetter(models.Model):

    text = models.CharField(max_length=50, default="")
    status = models.IntegerField(default=0)

    def __str__(self):

         return self.text