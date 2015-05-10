from rest_framework import serializers
from ft_fitting.models import Fitting, Ingredient, Ask


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        excludes = kwargs.pop('exclude_fields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if excludes is not None:
            excluded = set(excludes)
            for field_name in excluded:
                self.fields.pop(field_name)


class IngredientSerializer(serializers.ModelSerializer):
    fitting = serializers.IntegerField(write_only=True)
    like_count = serializers.SerializerMethodField()

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

    def get_like_count(self, obj):
        return obj.like_count


class FittingSerializer(DynamicFieldsModelSerializer):
    ingredients = IngredientSerializer(many=True)
    picture = serializers.URLField()
    like_count = serializers.SerializerMethodField()

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

    def get_like_count(self, obj):
        return obj.like_count


class AskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Ask