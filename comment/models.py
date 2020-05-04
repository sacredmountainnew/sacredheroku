from __future__ import unicode_literals
from django.db import models

# Create your models here.
#from __future__ import unicode_literals(This module is to support all languages)

class Comment(models.Model):
   
    comment = models.TextField()
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    news_pk = models.IntegerField()
    date = models.CharField(max_length=12)
    time = models.CharField(max_length=5)
    status = models.IntegerField(default=0)

    def __str__(self):

        return self.name