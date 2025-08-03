from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.forms import AppUserCreateForm, AppLoginForm, ProfileEditForm
from accounts.models import Profile

# Create your views here.
UserModel = get_user_model()


class AppUserCreateView(CreateView):
    model = UserModel
    form_class = AppUserCreateForm
    template_name = 'accounts/register-template.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form: AppUserCreateForm) -> HttpResponse:
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        return response


class AppLoginView(LoginView):
    form_class = AppLoginForm

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy(
            'dashboard', kwargs={'pk': user.pk}
        )


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-template.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy(
            'dashboard', kwargs={'pk': user.pk}
        )
