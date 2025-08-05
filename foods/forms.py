from datetime import datetime

from django import forms

from django.utils.timezone import now
from foods.choices import MealTypeChoices
from foods.models import Food, Meal, Tag


class FoodBaseForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'


class FoodCreateForm(FoodBaseForm):
    class Meta(FoodBaseForm.Meta):
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }


class FoodEditForm(FoodBaseForm):
    class Meta(FoodBaseForm.Meta):
        exclude = ['id']


class FoodDeleteForm(FoodBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'image':
                continue  # We'll handle image separately in the template
            field.widget.attrs['readonly'] = True


class AddFoodToMealForm(forms.Form):
    grams = forms.IntegerField(min_value=1)
    meal_type = forms.ChoiceField(choices=MealTypeChoices.choices)
    date = forms.DateField(initial=now().date)


class BaseTagsForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class TagsCreateForm(BaseTagsForm):
    pass
