""" Restaurant Location Model """
from django.db import models
from django.db.models import Avg
from .review import Review

class RestaurantLocation(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='restaurants')
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='locations')
    hours = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    @property
    def location_average_rating(self):
        avg_score = Review.objects.filter(restaurant_location = self).aggregate(Avg('score'))['score__avg'] or 0
        return round(avg_score, 2)
