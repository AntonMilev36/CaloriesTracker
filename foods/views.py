import datetime

from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from foods.choices import MealTypeChoices
from foods.forms import FoodCreateForm
from foods.models import Food, Meal


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


class DailyDashboardView(TemplateView):
    template_name = 'food/daily-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        date = datetime.datetime.today()

        meals = {}
        daily_cals = 0

        for meal in MealTypeChoices:
            meal_type = meal.label
            meal_obj = Meal.objects.filter(
                user=self.request.user,
                meal_type=meal_type,
                date=date
            ).first()

            meals[meal_type] = meal_obj
            daily_cals = sum(m.meal_cal for m in meals.values() if m is not None)

        context['date'] = date
        context['meal_type'] = meals
        context['daily_cals'] = daily_cals

        return context
