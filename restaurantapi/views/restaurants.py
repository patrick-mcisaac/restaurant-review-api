from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from restaurantapi.models import Restaurant, Review

class Restaurants(ViewSet):
    def list(self, request):
        restaurants = Restaurant.objects.all()
        ser = RestaurantSerializer(restaurants, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
    
    def retrieve(self,request,pk = None):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            ser = RestaurantSerializer(restaurant, many=False)
            return Response(ser.data, status=status.HTTP_200_OK)
        except Restaurant.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['review', 'user', 'restaurant_location']


class RestaurantSerializer(serializers.ModelSerializer):
    restaurant_reviews = ReviewSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ['id','average_ratings', 'name', 'description', 'restaurant_reviews']
