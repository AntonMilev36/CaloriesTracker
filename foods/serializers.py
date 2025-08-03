from rest_framework import serializers

from foods.models import Food


class FoodSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'
