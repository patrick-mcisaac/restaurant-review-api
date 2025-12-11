from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from restaurantapi.models import Restaurant, Review, RestaurantLocation, Rating
from .locations import LocationSerializer 
from django.contrib.auth.models import User

class Restaurants(ViewSet):
    def list(self, request):
        restaurants = Restaurant.objects.all()
        ser = RestaurantSerializer(restaurants, many=True, context={'restaurants': restaurants, 'user': request.auth.user})
        return Response(ser.data, status=status.HTTP_200_OK)

    def retrieve(self,request,pk = None):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            ser = RestaurantSerializer(restaurant, many=False, context={'restaurant': restaurant, 'user': request.auth.user})
            return Response(ser.data, status=status.HTTP_200_OK)
        except Restaurant.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

class ReviewSerializer(serializers.ModelSerializer):


    class Meta:
        model = Review
        fields = ['review', 'user', 'restaurant_location']



class RestaurantLocationSerializer(serializers.ModelSerializer):

    location = LocationSerializer(many=False)

    class Meta:
        model = RestaurantLocation
        fields = ['id', 'location', 'hours', 'address']

class RestaurantSerializer(serializers.ModelSerializer):
    user_score = serializers.SerializerMethodField()
    restaurant_reviews = ReviewSerializer(many=True)
    locations = RestaurantLocationSerializer(many=True)
    class Meta:
        model = Restaurant
        fields = ['id','average_ratings', 'name', 'description', 'restaurant_reviews', 'locations', 'image','user_score']
    
    def get_user_score(self, obj):

        restaurant = obj
        try:
            user_rating = Rating.objects.get(user=self.context['user'], restaurant=restaurant)
            return user_rating.score
        except Rating.DoesNotExist:
            return 0
