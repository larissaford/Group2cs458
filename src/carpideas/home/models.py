from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Quotes(models.Model):
	quotesID = models.CharField(max_length=16, primary_key= True)
	quote = models.CharField(max_length=300)

	#def __str__(self):
	#	return self.quote