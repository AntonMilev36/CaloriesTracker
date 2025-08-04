from django.contrib import admin
from foods.models import Food, Meal

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'protein', 'carbs', 'fats')
    search_fields = ('name',)


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_type', 'date', 'total_calories',)
    list_filter = ('meal_type', 'date', 'user')
    date_hierarchy = 'date'
    search_fields = ('meal_type',)

    def total_calories(self, obj):
        return obj.meal_cal
    total_calories.short_description = 'Calories'
