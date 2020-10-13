from django.db import models

# Create your models here.
class Image(models.Model):
    imageID = models.CharField(max_length=16, primary_key= True)
    url = models.URLField()
    width = models.IntegerField()
    height = models.IntegerField()