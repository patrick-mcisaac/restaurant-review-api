""" model for ratings """
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Rating(models.Model):
    score = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE, related_name='restaurant_ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant_ratings')
