from django.db import models

class DiningExperience(models.Model):
    description = models.CharField(max_length=255)
