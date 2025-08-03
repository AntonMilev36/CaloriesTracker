from django.urls import path, include

from foods.views import FoodCreateView, DailyDashboardView, FoodListView, FoodsListAPIView

urlpatterns = [
    path('add/', FoodCreateView.as_view(), name='create-food'),
    path('list/', FoodListView.as_view(), name='food-list'),
    path('api/foods/', FoodsListAPIView.as_view(), name='food-search-api'),
    path('<int:pk>/', include([
        path('dashboard/', DailyDashboardView.as_view(), name='dashboard'),

    ]))
]
