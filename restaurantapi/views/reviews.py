from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from restaurantapi.models import Review, Restaurant, City, RestaurantLocation
from django.contrib.auth.models import User

class Reviews(ViewSet):
    def list(self, request):
        restaurant_id = request.query_params.get('restaurant', None)
        if restaurant_id is not None:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            reviews = Review.objects.filter(restaurant_location__restaurant=restaurant)
            ser = ReviewSerializer(reviews, many=True, context={'user': request.auth.user})
            return Response(ser.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            ser = ReviewSerializer(review, many=False, context={'user': request.auth.user})
            return Response(ser.data, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        restaurant = Restaurant.objects.get(pk=request.data.get('restaurant'))
        city = RestaurantLocation.objects.get(pk=request.data.get('city'))
        review = Review(
            review = request.data.get('review', None),
            score = request.data.get('score', None),
            restaurant = restaurant,
            restaurant_location = city,
            user = request.auth.user
        )
        try:
            review.full_clean()
            review.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({'Error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class RestaurantReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['id','name']


class UserReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserReviewSerializer()
    restaurant_location = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return obj.user == self.context['user']


    def get_restaurant_location(self, obj):
        city = City.objects.get(pk=obj.restaurant_location.city_id)
        return {'id':city.id,'city':city.name}
    class Meta:
        model = Review
        fields = ['id', 'review', 'score', 'user', 'restaurant_location', 'is_owner']
