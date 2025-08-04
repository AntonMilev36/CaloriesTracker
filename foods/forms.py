from datetime import datetime

from django import forms

from django.utils.timezone import now
from foods.choices import MealTypeChoices
from foods.models import Food


class FoodBaseForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'


class FoodCreateForm(FoodBaseForm):
    pass


class AddFoodToMealForm(forms.Form):
    grams = forms.IntegerField(min_value=1)
    meal_type = forms.ChoiceField(choices=MealTypeChoices.choices)
    date = forms.DateField(initial=now().date)

