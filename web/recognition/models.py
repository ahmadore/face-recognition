from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Report(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200)
    address = models.TextField()
    photo = models.ImageField(upload_to='images')