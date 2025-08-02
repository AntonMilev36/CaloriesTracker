from django.db import models


class MealTypeChoices(models.TextChoices):
    BREAKFAST = 'b', 'Breakfast'
    LUNCH = 'l', 'Lunch'
    DINNER = 'd', 'Dinner'
    SNACKS = 's', 'Snacks'
