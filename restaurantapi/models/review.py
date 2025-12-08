""" Review model """
from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    review = models.TextField()
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE, related_name='restaurant_reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant_reviews')
    restaurant_location = models.ForeignKey('RestaurantLocation', on_delete=models.CASCADE, related_name='review')
