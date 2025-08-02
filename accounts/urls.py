from django.contrib.auth.views import LogoutView
from django.urls import path, include

from accounts.views import AppUserCreateView, AppLoginView, ProfileEditView

urlpatterns = [
    path('register/', AppUserCreateView.as_view(), name='register'),
    path('login/', AppLoginView.as_view(template_name='accounts/login-template.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', include([
        path('edit/' ,ProfileEditView.as_view(), name='edit_profile')
    ]))
]
