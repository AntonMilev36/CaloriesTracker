from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now

from foods.choices import MealTypeChoices


# Create your models here.
UserModel = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True
    )

    def __str__(self):
        return self.name


class Food(models.Model):

    name = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(2)
        ],
        unique=True
    )

    image = models.URLField(
        null=True
    )

    # All macros are per 100 grams
    calories = models.FloatField(
        validators=[
            MinValueValidator(1)
        ]
    )

    protein = models.FloatField(
        validators=[
            MinValueValidator(1)
        ]
    )

    carbs = models.FloatField(
        validators=[
            MinValueValidator(1)
        ]
    )

    fats = models.FloatField(
        validators=[
            MinValueValidator(1)
        ]
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True
    )

    def __str__(self):
        return self.name


class Meal(models.Model):
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE
    )

    meal_type = models.CharField(
        max_length=10,
        choices=MealTypeChoices.choices,
        default=MealTypeChoices.SNACKS
    )

    date = models.DateField(
        default=now
    )

    foods = models.ManyToManyField(
        to=Food,
        through='MealFood',
        name='meal'
    )

    def get_current_meal(self):
        return MealFood.objects.filter(meal=self)

    @property
    def meal_cal(self):
        curr_meal = self.get_current_meal()
        return sum(m.food_cal for m in curr_meal)

    @property
    def meal_protein(self):
        curr_meal = self.get_current_meal()
        return sum(m.food_protein for m in curr_meal)

    @property
    def meal_carbs(self):
        curr_meal = self.get_current_meal()
        return sum(m.food_carbs for m in curr_meal)

    @property
    def meal_fats(self):
        curr_meal = self.get_current_meal()
        return sum(m.food_fats for m in curr_meal)

    def __str__(self):
        return self.meal_type


class MealFood(models.Model):
    meal = models.ForeignKey(
        to=Meal,
        on_delete=models.CASCADE
    )

    food = models.ForeignKey(
        to=Food,
        on_delete=models.PROTECT
    )

    grams_of_food = models.PositiveIntegerField()

    # class Meta:
    #     unique_together = ('meal', 'food')

    def food_macros(self, macros_type):
        return (macros_type / 100) * self.grams_of_food

    @property
    def food_cal(self):
        return self.food_macros(self.food.calories)

    @property
    def food_protein(self):
        return self.food_macros(self.food.protein)

    @property
    def food_carbs(self):
        return self.food_macros(self.food.carbs)

    @property
    def food_fats(self):
        return self.food_macros(self.food.fats)
