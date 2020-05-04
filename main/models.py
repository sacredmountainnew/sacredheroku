from __future__ import unicode_literals
from django.db import models

# Create your models here.
#from __future__ import unicode_literals(This module is to support all languages)

class Main(models.Model):
    name = models.CharField(max_length=30)
    about = models.TextField()
    aboutdetail = models.TextField(default="")
    fb = models.CharField(max_length=30)
    tw = models.CharField(max_length=30)
    yt = models.CharField(max_length=30)
    tel = models.CharField(max_length=30)
    link = models.CharField(max_length=30)
    picurlfoot = models.TextField(default="")
    picnamefoot = models.TextField(default="")
    picurlhead = models.TextField(default="")
    picnamehead = models.TextField(default="")
    
    set_name = models.CharField(max_length=30)

    def __str__(self):
       return self.set_name + " | " + str(self.pk)
        