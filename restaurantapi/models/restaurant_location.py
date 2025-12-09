""" Restaurant Location Model """
from django.db import models

class RestaurantLocation(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='restaurants')
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='locations')
    hours = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
