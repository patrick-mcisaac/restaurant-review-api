from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from restaurantapi.models import DiningExperience


class DiningExperienceAPITests(APITestCase):
    """
    Test API requests and response for Dining Experiences
    """

    def setUp(self):
        self.experience = DiningExperience(description="test description")
        self.experience.save()

        self.user = User.objects.create_user(username="testUser", password="password")

        self.url = reverse("experience-list")

        self.client.force_authenticate(user=self.user)

    def test_experience_get_request(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
