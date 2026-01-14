from django.test import TestCase
from django.core.exceptions import ValidationError
from restaurantapi.models import DiningExperience


class RestaurantExperienceTests(TestCase):
    """
    Test Experience Model
    """

    def test_dining_experience_model(self):
        experience = DiningExperience(description="test description")

        self.assertEqual(experience.description, "test description")

    def test_save_experience(self):
        experience = DiningExperience(description="did it save")

        experience.save()

        self.assertEqual(DiningExperience.objects.count(), 1)
        self.assertTrue(
            DiningExperience.objects.filter(description="test description").exists
        )

    def test_null_data(self):
        experience = DiningExperience()

        with self.assertRaises(ValidationError):
            experience.full_clean()

    def test_bad_data(self):

        experience = DiningExperience(description="123" * 100)

        with self.assertRaises(ValidationError):
            experience.full_clean()
