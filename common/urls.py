from django.urls import path, include

from common.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home')
]