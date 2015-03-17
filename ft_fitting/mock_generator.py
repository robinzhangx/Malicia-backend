# coding=utf-8
from itertools import groupby
import random
from fitting.mock_generator import MockGeneratorBase
from ft_fitting.models import Fitting, Ingredient


class MockGenerator(MockGeneratorBase):
    fitting_titles = [
        u'花枝招展啊',
        u'帅的一塌糊涂',
        u'看了一眼，就再也不敢看了',
        u'逼格报表了么',
        u'哈哈哈哈，已瞎',
        u'宇宙无敌第一帅',
        u'算了，想不出了',
    ]

    ingredient_size = [
        u'S',
        u'SM',
        u'M',
        u'L',
        u'XL',
        u'XXL',
        u'XXXL',
    ]

    @classmethod
    def generate_fittings(cls, clear=False, count=100):
        if clear:
            Fitting.objects.all().delete()

        for i in xrange(0, count):
            fitting = Fitting()
            fitting.user = cls.random_user().next()
            fitting.bmi = fitting.user.bmi
            fitting.title = cls.pick_one(cls.fitting_titles)

            fitting.save()

    @classmethod
    def generate_ingredients(cls, clear=False, count=400):
        if clear:
            Ingredient.objects.all().delete()

        parts = [i[0] for i in Ingredient.Part_Choices]
        for i in xrange(0, count):
            ingredient = Ingredient()
            ingredient.part = cls.pick_one(parts)
            ingredient.size = cls.pick_one(cls.ingredient_size)
            ingredient.user = cls.random_user().next()
            ingredient.save()

    @classmethod
    def generate_relation_fitting_ingredient(cls):
        ingredients = Ingredient.objects.all()

        ingredients_map = groupby(ingredients, lambda x: x.part)

        for part, ingredients in ingredients_map:
            for i in ingredients:
                fittings = i.user.fittings.all()

                count = random.randint(1, 4)
                for x in xrange(0, count):
                    fitting = cls.pick_one(fittings)
                    if fitting is not None:
                        i.fittings.add(fitting)
                i.save()
