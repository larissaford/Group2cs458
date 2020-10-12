from django.db import models

# Create your models here.
class Image(models.Model):
    imageId = models.CharField(max_length=16, primary_key= True)
    url = models.URLField(max_length=200)
    width = models.IntegerField()
    height = models.IntegerField()