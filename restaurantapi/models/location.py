""" location model """

from django.db import models

class Location(models.Model):
    city = models.CharField(max_length=255)
