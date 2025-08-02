from django import forms

from foods.models import Food


class FoodBaseForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'


class FoodCreateForm(FoodBaseForm):
    pass

