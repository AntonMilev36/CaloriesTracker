from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.db import models

from accounts.choices import GenderChoices
from accounts.managers import AppUserManager


# Create your models here.

class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True
    )

    is_active = models.BooleanField(
        default=True,
        blank=True
    )

    is_staff = models.BooleanField(
        default=False,
        blank=True
    )

    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Profile(models.Model):
    user = models.OneToOneField(
        to=AppUser,
        on_delete=models.CASCADE,
        primary_key=True
    )

    first_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2)
        ],
        null=True,
        blank=True
    )

    last_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2)
        ],
        null=True,
        blank=True
    )

    age = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(200)
        ],
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=7,
        choices=GenderChoices.choices,
        null=True,
        blank=True
    )
