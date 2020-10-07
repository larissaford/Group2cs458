from django.db import models
from .models import *



# Create your models here.
class Contains(models.Model):
    accountImages = models.ManyToManyField("Image.Image")
