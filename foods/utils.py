from django.urls import path, include

from foods.views import FoodCreateView, DailyDashboardView

urlpatterns = [
    path('add/', FoodCreateView.as_view(), name='create-food'),
    path('<int:pk>/', include([
        path('dashboard/', DailyDashboardView.as_view(), name='dashboard')
    ]))
]
