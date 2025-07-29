from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.fields import EmailField

from accounts.models import Profile

UserModel = get_user_model()


class AppUserCreateForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email',)
        field_classes = {'email': EmailField}


class AppLoginForm(AuthenticationForm):
    username = EmailField


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'age', 'gender']

