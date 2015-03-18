# coding=utf-8
from ft_accounts.models import User
from django.db import models


class Fitting(models.Model):
    """
    The fitting contains several ingredients
    """

    user = models.ForeignKey(User, related_name='fittings')
    bmi = models.FloatField(u'当时的BMI', default=22)
    title = models.CharField(u'题目', max_length=256)
    picture = models.ImageField(u'图片', upload_to='fitting')
    created_at = models.DateTimeField(u'发布时间', auto_now_add=True)

    like_count = models.IntegerField(u'喜爱', default=0)


class Ingredient(models.Model):
    Part_Cloths = u'上装'
    Part_Pant = u'下装'
    Part_Shoe = u'鞋'
    Part_Bag = u'包'
    Part_Other = u'配件'

    Part_Choices = (
        (Part_Cloths, Part_Cloths),
        (Part_Pant, Part_Pant),
        (Part_Shoe, Part_Shoe),
        (Part_Bag, Part_Bag),
        (Part_Other, Part_Other),
    )

    fittings = models.ManyToManyField(Fitting, related_name="ingredients")
    user = models.ForeignKey(User, related_name="ingredients")

    created_at = models.DateTimeField(u'创建时间', auto_now_add=True)
    part = models.CharField(u'部件名称', max_length=32, choices=Part_Choices, null=True, blank=True, db_index=True)
    size = models.CharField(u'尺码', max_length=32, null=True, blank=True)

    like_count = models.IntegerField(u'喜爱数', default=0)

    def __unicode__(self):
        return u'%s: %s' % (self.id, self.part)


class Ask(models.Model):
    ingredient = models.ForeignKey(Ingredient, related_name='asks')
    user = models.ForeignKey(User, related_name='asks')
    content = models.TextField(u'询问内容', null=True, blank=True)
    answered = models.BooleanField(u'是否回答', default=False)

    created_at = models.DateTimeField(u'询问时间', auto_now_add=True)


class FittingForDiscover(models.Model):
    fitting = models.OneToOneField(Fitting, related_name='discover')
    created_at = models.DateTimeField(auto_now_add=True)
