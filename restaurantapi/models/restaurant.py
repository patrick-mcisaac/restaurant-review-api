""" models for restaurants """

from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    hours = models.CharField(max_length=255)
    address= models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    location = models.ManyToManyField('Location', related_name='restaurants')
    ratings = models.ManyToManyField(User, through='Rating', related_name='ratings')
    reviews = models.ManyToManyField(User, through='Review', related_name='reviews')
