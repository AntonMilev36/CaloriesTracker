from django.test import TestCase
from foods.models import Food

# Create your tests here.

class FoodModelTest(TestCase):
    def setUp(self):
        self.food = Food.objects.create(
            name = "Steak",
            image = "https://pngimg.com/d/steak_PNG61.png",
            calories = 156,
            protein = 52,
            carbs = 33,
            fats = 358000,
        )

    def test__food_str_method_name_return(self):
        self.assertEqual(str(self.food), "Steak")
