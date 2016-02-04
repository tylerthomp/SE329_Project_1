from __future__ import unicode_literals

from django.db import models


class Person(models.Model):
    uid = models.CharField(max_length=128, primary_key=True, unique=True)
    name = models.CharField(max_length=128)

# Create your models here.
