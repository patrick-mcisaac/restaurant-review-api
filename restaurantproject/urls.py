from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from restaurantapi.views import Restaurants, Locations

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'restaurants', Restaurants, 'restaurant')
router.register(r'locations',Locations, 'location')

urlpatterns = [
    path('', include(router.urls)),
]
