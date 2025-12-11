from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from restaurantapi.models import Review, Restaurant, Location
from django.contrib.auth.models import User

class Reviews(ViewSet):
    def list(self, request):
        restaurant_id = request.query_params.get('restaurant', None)
        if restaurant_id is not None:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            reviews = Review.objects.filter(restaurant=restaurant)
            ser = ReviewSerializer(reviews, many=True, context={'user': request.auth.user})
            return Response(ser.data, status=status.HTTP_200_OK)


class RestaurantReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['id','name']


class UserReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']

class ReviewSerializer(serializers.ModelSerializer):
    restaurant = RestaurantReviewSerializer()
    user = UserReviewSerializer()
    restaurant_location = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return obj.user == self.context['user']


    def get_restaurant_location(self, obj):
        location = Location.objects.get(pk=obj.restaurant_location.id)
        return location.city
    class Meta:
        model = Review
        fields = ['id', 'review', 'restaurant', 'user', 'restaurant_location', 'is_owner']
