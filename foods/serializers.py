from rest_framework import serializers

from foods.models import Food


class FoodSearchSerializer(serializers.ModelSerializer):
    can_edit = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = ['id', 'name', 'image', 'calories', 'protein', 'carbs', 'fats', 'tags', 'can_edit']

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_can_edit(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_staff and request.user.is_superuser
        return False

