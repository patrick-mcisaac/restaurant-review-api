from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from restaurantapi.models import Review, Restaurant, Location, RestaurantLocation
from django.contrib.auth.models import User

class Reviews(ViewSet):
    def list(self, request):
        restaurant_id = request.query_params.get('restaurant', None)
        if restaurant_id is not None:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            reviews = Review.objects.filter(restaurant=restaurant)
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
        location = RestaurantLocation.objects.get(pk=request.data.get('location'))
        review = Review(
            review = request.data.get('review'),
            restaurant = restaurant,
            restaurant_location = location,
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
    restaurant = RestaurantReviewSerializer()
    user = UserReviewSerializer()
    restaurant_location = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return obj.user == self.context['user']


    def get_restaurant_location(self, obj):
        location = Location.objects.get(pk=obj.restaurant_location.id)
        return {'id':location.id,'city':location.city}
    class Meta:
        model = Review
        fields = ['id', 'review', 'restaurant', 'user', 'restaurant_location', 'is_owner']

# class CreateReviewSerializer(serializers.ModelSerializer):

#     restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
#     restaurant_location = serializers.PrimaryKeyRelatedField(queryset=RestaurantLocation.objects.all())
#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

#     class Meta:

#         model = Review
#         fields = ['review', 'restaurant', 'user', 'restaurant_location']
