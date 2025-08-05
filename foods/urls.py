from django.urls import path, include

from foods.views import FoodCreateView, DailyDashboardView, FoodListView, FoodsListAPIView, AddFoodToMealView, \
    MealDetailView, FoodEditView, FoodDeleteView, CreateTagView

urlpatterns = [
    path('add/', FoodCreateView.as_view(), name='create-food'),
    path('add/tag/', CreateTagView.as_view(), name='create-tag'),
    path('list/', FoodListView.as_view(), name='food-list'),
    path('api/foods/', FoodsListAPIView.as_view(), name='food-search-api'),
    path('meals/<str:meal_type>/<str:date>/', MealDetailView.as_view(), name='meal-detail'),

    path('<int:pk>/', include([
        path('dashboard/', DailyDashboardView.as_view(), name='dashboard'),
        path('add-to-meal/', AddFoodToMealView.as_view(), name='add-food-to-meal'),
        path('edit/', FoodEditView.as_view(), name='edit-food'),
        path('delete/', FoodDeleteView.as_view(), name='delete-food')
    ]))
]
