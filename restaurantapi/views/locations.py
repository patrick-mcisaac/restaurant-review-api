from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from restaurantapi.models import Location

class Locations(ViewSet):
    def list(self, request):
        locations = Location.objects.all()
        ser = LocationSerializer(locations, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            location = Location.objects.get(pk=pk)
            ser = LocationSerializer(location, many=False)
            return Response(ser.data, status=status.HTTP_200_OK)
        except Location.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['id', 'city',]
