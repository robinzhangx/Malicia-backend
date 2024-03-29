# coding=utf-8
from itertools import groupby
import random
from fitting.mock_generator import MockGeneratorBase
from ft_fitting.models import Fitting, Ingredient, LikeFitting, LikeIngredient, Ask, Brand


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

    brands = [
        u'Nike',
        u'M2M',
        u'Puma',
        u'Ralph R',
        u'Jack Jones',
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
    def generate_brand(cls, clear=False):
        if clear:
            Brand.objects.all().delete()

        for brand_name in cls.brands:
            brand = Brand(name=brand_name)
            brand.save()


    @classmethod
    def generate_ingredients(cls, clear=False, count=400):
        if clear:
            Ingredient.objects.all().delete()

        parts = [i[0] for i in Ingredient.Part_Choices]
        brands = Brand.objects.all()
        for i in xrange(0, count):
            ingredient = Ingredient()
            ingredient.part = cls.pick_one(parts)
            ingredient.size = cls.pick_one(cls.ingredient_size)
            ingredient.user = cls.random_user().next()
            ingredient.picture = "http://g.hiphotos.baidu.com/image/w%3D310/sign=042b0836dbf9d72a1764161ce42b282a/adaf2edda3cc7cd9937758d03b01213fb80e9164.jpg"
            ingredient.brand = cls.pick_one(brands)
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

    @classmethod
    def generate_like_fitting(cls):
        fittings = Fitting.objects.all()
        for i in xrange(0, 100):
            try:
                user = cls.random_user().next()
                fitting = cls.pick_one(fittings)
                like = LikeFitting()
                like.fitting = fitting
                like.user = user
                like.save()
            except:
                pass

    @classmethod
    def generate_like_ingredient(cls):
        ingredients = Ingredient.objects.all()
        for i in xrange(0, 100):
            try:
                user = cls.random_user().next()
                fitting = cls.pick_one(ingredients)
                like = LikeIngredient()
                like.fitting = fitting
                like.user = user
                like.save()
            except:
                pass

    @classmethod
    def generate_likes(cls):
        cls.generate_like_fitting()
        cls.generate_like_ingredient()

    @classmethod
    def generate_asks(cls):
        ingredients = Ingredient.objects.all()

        asks = [
            "What is the size of this?",
            u"为什么穿起来这么屌",
            u"你这个裙子有点夸张啊",
            u"无言以对",
            u"真的是这么穿么",
        ]

        for i in ingredients:
            for _ in xrange(0, 2):
                ask = Ask()
                ask.ingredient = i
                ask.user = cls.random_user().next()
                ask.content = cls.pick_one(asks)
                ask.save()

    @classmethod
    def create_fitting(cls, user):
        fitting = Fitting()
        fitting.user = user
        fitting.bmi = user.bmi
        fitting.title = 'test title'
        fitting.picture = 'http://www.baidu.com'
        fitting.save()
        return fitting

    @classmethod
    def create_ingredient(cls, user):
        ingredient = Ingredient()
        ingredient.part = Ingredient.Part_Cloths
        ingredient.size = u'超级大'
        ingredient.user = user
        ingredient.save()
        return ingredient
