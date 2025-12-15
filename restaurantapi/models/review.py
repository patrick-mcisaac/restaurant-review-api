""" Review model """
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    review = models.TextField(null=True, blank=True)
    score = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant_reviews')
    restaurant_location = models.ForeignKey('RestaurantLocation', on_delete=models.CASCADE, related_name='review')
    dining_experience = models.ManyToManyField('DiningExperience')