from rest_framework import serializers
from ft_fitting.models import Fitting, Ingredient, Ask


class IngredientSerializer(serializers.ModelSerializer):
    fitting = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ingredient
        read_only_fields = ('user', 'created_at', 'like_count')

    def create(self, validated_data):
        fitting_id = validated_data['fitting']
        fitting = Fitting.objects.get(id=fitting_id)
        ingredient = Ingredient()
        ingredient.user = self.context['request'].user
        ingredient.part = validated_data['part']
        ingredient.size = validated_data['size']
        ingredient.save()

        ingredient.fittings.add(fitting)
        ingredient.save()
        return ingredient


class FittingSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    picture = serializers.URLField()

    class Meta:
        model = Fitting
        read_only_fields = ('user', 'bmi', 'like_count', 'created_at')

    def create(self, validated_data):
        fitting = Fitting()
        fitting.user = self.context['request'].user
        fitting.title = validated_data['title']
        fitting.picture = validated_data['picture']
        fitting.bmi = fitting.user.bmi
        fitting.save()
        return fitting


class AskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ask