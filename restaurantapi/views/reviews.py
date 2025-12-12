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
        city = RestaurantLocation.objects.get(pk=request.data.get('location'))
        review = Review(
            review = request.data.get('review', None),
            score = request.data.get('score', None),
            restaurant_location = city,
            user = request.auth.user
        )
        try:
            review.full_clean()
            review.save()
            return Response(None, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({'Error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            self.check_object_permissions(request=request, obj=review)
            review.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as ex:
            return Response({"error": str(ex)}, status=status.HTTP_401_UNAUTHORIZED)


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
    restaurant = serializers.SerializerMethodField()

    def get_restaurant(self, obj):
        restaurant = Restaurant.objects.get(pk = obj.restaurant_location.restaurant.id)
        ser = RestaurantReviewSerializer(restaurant)
        return ser.data
    def get_is_owner(self, obj):
        return obj.user == self.context['user']


    def get_restaurant_location(self, obj):
        city = City.objects.get(pk=obj.restaurant_location.city_id)
        return {'id':city.id,'name':city.name}
    class Meta:
        model = Review
        fields = ['id', 'review', 'score', 'user', 'restaurant_location', 'is_owner', 'restaurant']
