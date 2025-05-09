from django.db import models


# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
