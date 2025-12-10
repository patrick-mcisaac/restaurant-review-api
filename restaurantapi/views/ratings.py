from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action
from restaurantapi.models import Rating, Restaurant

class Ratings(ViewSet):

    @action(methods=['post'], detail=False, url_path='add_rating' )
    def add_rating(self, request):
        restaurant = Restaurant.objects.get(pk=request.data.get('restaurant'))
        try:
            rating = Rating.objects.get(user=request.auth.user, restaurant=restaurant)
            rating.score = request.data.get('score')
            rating.full_clean()
            rating.save()
            ser = UpdateRatingSerializer(rating, many=False, context={'request': request, 'restaurant': request.data.get('restaurant')})
            return Response(ser.data, status=status.HTTP_200_OK)

        except Rating.DoesNotExist:
            rating = Rating()
            rating.score = request.data.get('score')
            rating.restaurant = restaurant
            rating.user=request.auth.user
            rating.full_clean()
            rating.save()
            ser = UpdateRatingSerializer(rating, many=False, context={'request': request, 'restaurant': request.data.get('restaurant')})
            return Response(ser.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"Error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)



class UpdateRatingSerializer(serializers.ModelSerializer):

    new_avg = serializers.SerializerMethodField()

    def get_new_avg(self, obj):
        restaurant = Restaurant.objects.get(pk=self.context['restaurant'])
        return restaurant.average_ratings

    class Meta:
        model = Rating
        fields = ['id', 'score', 'restaurant', 'user', 'new_avg']
