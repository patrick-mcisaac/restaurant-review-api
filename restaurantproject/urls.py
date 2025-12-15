from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from restaurantapi.views import Restaurants, Reviews, Cities, Auth, DiningExperiences

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'restaurants', Restaurants, 'restaurant')
router.register(r'cities', Cities, 'city')
router.register(r'reviews', Reviews, 'review')
router.register(r'experiences', DiningExperiences, 'experience')


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls ),
    path('login', Auth.as_view({'post': 'login'}), name='login'),
    path('register', Auth.as_view({'post': 'register'}), name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
