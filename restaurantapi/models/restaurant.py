""" models for restaurants """

from django.db import models
from django.contrib.auth.models import User
from .rating import Rating



class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    ratings = models.ManyToManyField(User, through='Rating', related_name='ratings')
    reviews = models.ManyToManyField(User, through='Review', related_name='reviews')
    # TODO: make a seperate image model so i can have many images
    image = models.ImageField(upload_to='images', width_field=None, height_field=None, blank=True, null=True)

    @property
    def average_ratings(self):
        return Rating.objects.filter(restaurant=self).aggregate(models.Avg('score'))['score__avg'] or 0
