from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#class Image(models.Model):
 #   imageID = models.CharField(max_length=16, primary_key= True)
  #  url = models.URLField()
   # width = models.IntegerField()
    #height = models.IntegerField()
    #users = models.ManyToManyField(User, related_name='liked_images')
    #users = models.ManyToManyField(User, related_name='skipped_images')
    #def __unicode__(self):
    #    return self.name

class UserInput(models.Model):
    search = models.CharField(max_length)
    

class SearchURL(models.Model):
    url=models.URLField()
    seen = models.