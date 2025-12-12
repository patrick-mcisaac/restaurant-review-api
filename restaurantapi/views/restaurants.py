from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from restaurantapi.models import Restaurant, Review, RestaurantLocation, City
from .Cities import CitySerializer
from .reviews import ReviewSerializer


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

class RestaurantLocationSerializer(serializers.ModelSerializer):

    city=CitySerializer()

    class Meta:
        model = RestaurantLocation
        fields = ['id', 'city', 'hours', 'address', 'location_average_rating']


class RestaurantSerializer(serializers.ModelSerializer):
    locations = serializers.SerializerMethodField()

    def get_locations(self,obj):
        locations = RestaurantLocation.objects.filter(restaurant=obj)
        ser = RestaurantLocationSerializer(locations, many=True)
        return ser.data

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'image', 'average_ratings', 'locations']
