from django.db import models

# Create your models here.
class Image(models.Model):
    url = models.URLField(primary_key = True)
    width = models.IntegerField()
    height = models.IntegerField()