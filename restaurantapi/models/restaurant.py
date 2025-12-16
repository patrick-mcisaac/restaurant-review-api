"""models for restaurants"""

from django.db import models
from django.db.models import Avg
from .review import Review


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    # TODO: make a seperate image model so i can have many images
    image = models.ImageField(
        upload_to="images", width_field=None, height_field=None, blank=True, null=True
    )

    @property
    def average_ratings(self):
        avg_score = (
            Review.objects.filter(restaurant_location__restaurant=self).aggregate(
                Avg("score")
            )["score__avg"]
            or 0
        )
        return round(avg_score, 2)
