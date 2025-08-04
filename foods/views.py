import datetime

from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.timezone import localdate
from django.views.generic import CreateView, TemplateView, ListView, View
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from foods.choices import MealTypeChoices
from foods.forms import FoodCreateForm, AddFoodToMealForm
from foods.models import Food, Meal, MealFood
from foods.serializers import FoodSearchSerializer


# Create your views here.
class FoodCreateView(CreateView):
    model = Food
    form_class = FoodCreateForm
    template_name = 'food/add-food.html'

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy(
            'dashboard', kwargs={'pk': user.pk}
        )


class FoodsListAPIView(ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSearchSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class FoodListView(ListView):
    model = Food
    template_name = 'food/food-list.html'
    context_object_name = 'foods'


class DailyDashboardView(TemplateView):
    template_name = 'food/daily-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = localdate()

        meals = {}
        for meal_value, meal_label in MealTypeChoices.choices:
            # Fetch meal for user, date and meal type
            meal_instance = Meal.objects.filter(
                user=self.request.user,
                meal_type=meal_value,
                date=date
            ).first()
            meals[meal_label] = meal_instance

        daily_cals = sum(meal.meal_cal for meal in meals.values() if meal)

        context['date'] = date
        context['meals'] = meals
        context['daily_cals'] = daily_cals
        return context



class AddFoodToMealView(View):
    form_class = AddFoodToMealForm
    template_name = 'food/add-food-meal.html'

    def get(self, request, pk):
        food = get_object_or_404(Food, pk=pk)
        form = self.form_class(initial={
            'date': localdate(),
            'meal_type': MealTypeChoices.SNACKS,
            'grams': 100,
        })
        context = {
            'form': form,
            'food': food,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        food = get_object_or_404(Food, pk=pk)
        form = self.form_class(request.POST)
        if form.is_valid():
            grams = form.cleaned_data['grams']
            meal_type = form.cleaned_data['meal_type']
            date = form.cleaned_data['date']

            meal, created = Meal.objects.get_or_create(
                user=request.user,
                meal_type=meal_type,
                date=date,
            )

            MealFood.objects.create(
                meal=meal,
                food=food,
                grams_of_food=grams,
            )
            return redirect(reverse('dashboard', kwargs={'pk': request.user.pk}))

        return render(request, self.template_name, {'form': form, 'food': food})