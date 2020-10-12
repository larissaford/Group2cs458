from django.db import models
from Image.models import Image

# Create your models here.

class Account(models.Model):
    userID = models.CharField(max_length=16, primary_key= True)
    username = models.CharField(max_length=16) # we can discuss the max_length later
    password = models.CharField(max_length=50) # we can discuss the max_length later
    email = models.EmailField()
    images = models.ManyToManyField(Image)
    
#class accountImages(models.Model):
 #  account = models.ForeignKey('Account', on_delete=models.CASCADE)
  # image = models.ForeignKey('Image.Image',on_delete=models.CASCADE)
