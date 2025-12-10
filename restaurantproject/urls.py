from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from restaurantapi.views import Restaurants, Locations, Auth, Ratings

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'restaurants', Restaurants, 'restaurant')
router.register(r'locations',Locations, 'location')
router.register(r'ratings', Ratings, 'rating')


urlpatterns = [
    path('', include(router.urls)),
    path('login', Auth.as_view({'post': 'login'}), name='login'),
    path('register', Auth.as_view({'post': 'register'}), name='register'),
    path('add_rating', Ratings.as_view({'post':'add_rating'}, name='add_rating'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
