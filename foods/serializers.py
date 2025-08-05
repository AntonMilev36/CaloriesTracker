from rest_framework import serializers

from foods.models import Food


class FoodSearchSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Food
        fields = '__all__'
