from django.db import models

class GenderChoices(models.TextChoices):
    MALE = 'm', 'Male'
    FEMALE = 'f', 'Female'
    OTHER = 'o', 'Other'
