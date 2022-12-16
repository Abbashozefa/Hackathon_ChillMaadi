from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class ContactForm(models.Model):
    txt= models.CharField(max_length=100)  
    
    message= models.CharField(max_length=200)
