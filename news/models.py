from __future__ import unicode_literals
from django.db import models

# Create your models here.
#from __future__ import unicode_literals(This module is to support all languages)

class News(models.Model):
    
    name = models.CharField(max_length=100)
    short_text = models.TextField()
    body_text = models.TextField()
    date = models.CharField(max_length=12)
    time = models.CharField(max_length=12, default="00:00")
    picname = models.TextField()
    picurl = models.TextField(default="-")
    writer = models.CharField(max_length=50)
    subcatname = models.CharField(max_length=50, default='-')
    subcatid = models.IntegerField(default=0)
    catid = models.IntegerField(default=0)
    newsview = models.IntegerField(default=0)
    tag = models.TextField(default="")
    activate = models.IntegerField(default=0)
    rand = models.IntegerField(default=0)

    def __str__(self):
       return self.name