from __future__ import unicode_literals
from django.db import models

# Create your models here.
#from __future__ import unicode_literals(This module is to support all languages)

class ContactForm(models.Model):
   
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    message = models.TextField()
    date = models.CharField(max_length=12, default="")
    time = models.CharField(max_length=5, default="")

    def __str__(self):
       return self.name
    
    


   
        

# Create your models here.
