from django.db import models
from Image.models import Image
from accounts.models import Accounts


# Create your models here.
class Contains(models.Model):
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE,)
    image = models.ForeignKey(Image, on_delete=models.CASCADE,)