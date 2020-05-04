from __future__ import unicode_literals
from django.db import models

# Create your models here.
#from __future__ import unicode_literals(This module is to support all languages)

class BlackList(models.Model):
   
    ip = models.CharField(max_length=50)
  

    def __str__(self):
       return self.ip
