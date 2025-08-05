import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.timezone import localdate
from django.views.generic import CreateView, TemplateView, ListView, View, DetailView, UpdateView, DeleteView
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from foods.choices import MealTypeChoices
from foods.forms import FoodCreateForm, AddFoodToMealForm, FoodEditForm, FoodDeleteForm
from foods.models import Food, Meal, MealFood
from foods.serializers import FoodSearchSerializer


class DailyDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'food/daily-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = localdate()

        meals = []
        for meal_value, meal_label in MealTypeChoices.choices:
            meal_instance = Meal.objects.filter(
                user=self.request.user,
                meal_type=meal_value,
                date=date
            ).first()
            meals.append({
                'meal_label': meal_label,
                'meal_type': meal_value,
                'meal': meal_instance,
            })

        daily_cals = sum(m['meal'].meal_cal for m in meals if m['meal'])

        context['date'] = date
        context['meals'] = meals
        context['daily_cals'] = daily_cals
        return context


class FoodCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Food
    form_class = FoodCreateForm
    template_name = 'food/add-food.html'

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy(
            'dashboard', kwargs={'pk': user.pk}
        )

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('food-list')


class FoodsListAPIView(LoginRequiredMixin, ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSearchSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class FoodListView(ListView):
    model = Food
    template_name = 'food/food-list.html'
    context_object_name = 'foods'
    # paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        meal_type = self.kwargs.get('meal_type')
        context['meal_type'] = meal_type

        return context


class FoodEditView(UpdateView):
    model = Food
    form_class = FoodEditForm
    template_name = 'food/edit-food.html'
    success_url = reverse_lazy('food-list')


class FoodDeleteView(DeleteView):
    model = Food
    template_name = 'food/delete-food.html'
    success_url = reverse_lazy('food-list')


class MealDetailView(LoginRequiredMixin, DetailView):
    model = Meal
    template_name = 'food/meal-details.html'
    context_object_name = 'meal'

    def get_object(self, queryset=None):
        meal_type = self.kwargs['meal_type']
        date = self.kwargs['date']
        user = self.request.user

        valid_meal_types = [choice[0] for choice in MealTypeChoices.choices]
        if meal_type not in valid_meal_types:
            raise Http404("Invalid meal type")

        meal, created = Meal.objects.get_or_create(
            user=user,
            meal_type=meal_type,
            date=date,
        )
        return meal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meal = context['meal']
        context['meal_foods'] = meal.get_current_meal().select_related('food')
        context['meal_label'] = dict(MealTypeChoices.choices).get(meal.meal_type, meal.meal_type)
        context['date'] = meal.date
        return context


class AddFoodToMealView(LoginRequiredMixin, View):
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