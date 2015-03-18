from django.contrib import admin
from ft_fitting.models import Fitting, Ingredient, FittingForDiscover


@admin.register(Fitting)
class FittingAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'like_count', 'ingredients')
    search_fields = ('user__nickname', 'user__email')

    def nickname(self, obj):
        return obj.user.nickname

    def ingredients(self, obj):
        return [i for i in obj.ingredients.all()]

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'part', 'like_count', 'user')

    def user(self, obj):
        return obj.user.nickname

@admin.register(FittingForDiscover)
class FittingForDiscoverAdmin(admin.ModelAdmin):
    list_display = ('id', 'fitting_id')

    def fitting_id(self, obj):
        return obj.fitting.id
