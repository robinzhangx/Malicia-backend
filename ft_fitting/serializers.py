from rest_framework import serializers
from ft_fitting.models import Fitting, Ingredient, Ask


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient


class FittingSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    picture = serializers.URLField()

    class Meta:
        model = Fitting
        read_only_fields = ('user', 'bmi')

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