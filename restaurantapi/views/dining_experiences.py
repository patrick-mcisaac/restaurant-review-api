from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from restaurantapi.models import DiningExperience

class DiningExperiences(ViewSet):
    def list(self, request):
        experiences = DiningExperience.objects.all()
        ser = DiningExperienceSerializer(experiences, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class DiningExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiningExperience
        fields = ['id', 'description']