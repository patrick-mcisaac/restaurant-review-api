from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from restaurantapi.models import Review, Restaurant, City, RestaurantLocation
from .dining_experiences import DiningExperienceSerializer


class Reviews(ViewSet):
    def list(self, request):
        restaurant_id = request.query_params.get("restaurant", None)
        if restaurant_id is not None:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            reviews = Review.objects.filter(
                restaurant_location__restaurant=restaurant
            ).order_by("-created_at")
            ser = ReviewSerializer(
                reviews, many=True, context={"user": request.auth.user}
            )
            return Response(ser.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            ser = ReviewSerializer(
                review, many=False, context={"user": request.auth.user}
            )
            return Response(ser.data, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        city = RestaurantLocation.objects.get(
            city=request.data.get("location"), restaurant=request.data.get("restaurant")
        )
        review = Review(
            review=request.data.get("review", None),
            score=request.data.get("score", None),
            restaurant_location=city,
            user=request.auth.user,
        )
        experiences = request.data.get("dining_experience")
        checked_experiences = [
            experience["id"] for experience in experiences if experience["checked"]
        ]
        try:
            review.full_clean()
            review.save()
            review.dining_experience.set(checked_experiences)
            return Response(None, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"Error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            location = RestaurantLocation.objects.get(
                city=request.data.get("restaurant_location"),
                restaurant=request.data.get("restaurant"),
            )
            review.score = request.data.get("score")
            review.restaurant_location = location
            review.review = request.data.get("review")

            experiences = request.data.get("dining_experience")
            checked_experiences = [
                experience["id"] for experience in experiences if experience["checked"]
            ]

            review.full_clean()
            review.save()

            review.dining_experience.set(checked_experiences)
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
            self.check_object_permissions(request=request, obj=review)
            review.dining_experience.clear()
            review.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as ex:
            return Response({"error": str(ex)}, status=status.HTTP_401_UNAUTHORIZED)


class RestaurantReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ["id", "name"]


class UserReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username"]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserReviewSerializer()
    restaurant_location = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    restaurant = serializers.SerializerMethodField()
    dining_experience = DiningExperienceSerializer(many=True)

    def get_restaurant(self, obj):
        restaurant = Restaurant.objects.get(pk=obj.restaurant_location.restaurant.id)
        ser = RestaurantReviewSerializer(restaurant)
        return ser.data

    def get_is_owner(self, obj):
        return obj.user == self.context["user"]

    def get_restaurant_location(self, obj):
        city = City.objects.get(pk=obj.restaurant_location.city_id)
        return {"id": city.id, "name": city.name}

    class Meta:
        model = Review
        fields = [
            "id",
            "review",
            "score",
            "user",
            "restaurant_location",
            "is_owner",
            "restaurant",
            "dining_experience",
        ]
