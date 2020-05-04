from __future__ import unicode_literals
from django.db import models

class Trending(models.Model):

    text = models.CharField(max_length=200)


    def __str__(self):
        
        return self.text