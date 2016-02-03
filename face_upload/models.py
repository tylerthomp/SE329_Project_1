from __future__ import unicode_literals

from django.db import models

class Photo(models.Model):
    uid = models.CharField(max_length=128, primary_key=True, unique=True)

# Create your models here.
