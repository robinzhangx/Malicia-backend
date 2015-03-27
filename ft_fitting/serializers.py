from django.db.models import F
from rest_framework import serializers
from ft_fitting.models import Fitting, Ingredient, Ask, LikeFitting, LikeIngredient


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


class FittingSerializer(DynamicFieldsModelSerializer):
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


class LikeFittingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = LikeFitting

    def create(self, validated_data):
        like = super(LikeFittingSerializer, self).create(validated_data)

        like.fitting.like_count = F('like_count') + 1
        like.fitting.save()

        return like

    def to_representation(self, instance):
        rep = super(LikeFittingSerializer, self).to_representation(instance)
        rep['fitting'] = FittingSerializer(Fitting.objects.get(id=instance.fitting.id), exclude_fields=('ingredients',)).data
        return rep


class LikeIngredientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = LikeIngredient

    def create(self, validated_data):
        like = super(LikeIngredientSerializer, self).create(validated_data)

        like.ingredient.like_count = F('like_count') + 1
        like.ingredient.save()

        return like

    def to_representation(self, instance):
        rep = super(LikeIngredientSerializer, self).to_representation(instance)
        # The reason why we fetch the ingredient again is for like_count, it is a F expression which prevents
        # serializer works
        rep['ingredient'] = IngredientSerializer(Ingredient.objects.get(id=instance.ingredient.id)).data
        return rep
