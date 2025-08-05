from django.db import models


class MealTypeChoices(models.TextChoices):
    BREAKFAST = 'breakfast', 'Breakfast'
    LUNCH = 'lunch', 'Lunch'
    DINNER = 'dinner', 'Dinner'
    SNACKS = 'snacks', 'Snacks'
