from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from restaurantapi.models import City

class Cities(ViewSet):
    def list(self, request):
        restaurant = request.query_params.get('restaurant', None)
        if restaurant is not None:
            locations = City.objects.filter(restaurants__restaurant = restaurant)
            ser = CitySerializer(locations, many=True)
            return Response(ser.data, status=status.HTTP_200_OK)
        locations = City.objects.all()
        ser = CitySerializer(locations, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            location = City.objects.get(pk=pk)
            ser = CitySerializer(location, many=False)
            return Response(ser.data, status=status.HTTP_200_OK)
        except City.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['id', 'name',]
