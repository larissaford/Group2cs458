from django.db import models

# Create your models here.

class Account(models.Model):
    username = models.CharField(max_length=16) # we can discuss the max_length later
    password = models.CharField(max_length=50) # we can discuss the max_length later
    email = models.EmailField()
