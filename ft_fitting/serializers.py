from rest_framework import serializers
from ft_fitting.models import Fitting, Ingredient, Ask


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient


class FittingSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Fitting


class AskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ask