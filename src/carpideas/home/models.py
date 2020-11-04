from django.db import models


# Create your models here.
class Quote(models.Model):
	quoteID = models.CharField(max_length=16, primary_key= True)
	quote = models.CharField(max_length=300)

	def __str__(self):
		return self.quote