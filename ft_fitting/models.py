# coding=utf-8
from datetime import datetime
from django.dispatch import receiver
import pytz
from fitting.redis_store import redis_store
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

    def __unicode__(self):
        return self.title

    @property
    def like_count(self):
        return self.likefitting_set.all().count()


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

    def __unicode__(self):
        return u'%s: %s' % (self.id, self.part)

    @property
    def like_count(self):
        return self.likeingredient_set.all().count()


class LikeFitting(models.Model):
    user = models.ForeignKey(User)
    fitting = models.ForeignKey(Fitting)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('user', 'fitting')
        )
        ordering = "-created_at",

    def populate_cache(self):
        timestamp = (self.created_at - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
        redis_store.zadd('like_fitting_{0}'.format(self.user_id), timestamp, self.fitting_id)
        redis_store.zadd('fitting_followers_{0}'.format(self.fitting_id), timestamp, self.user_id)

    def remove_cache(self):
        redis_store.zrem('like_fitting_{0}'.format(self.user_id), self.fitting_id)
        redis_store.zrem('fitting_followers_{0}'.format(self.fitting_id), self.user_id)


@receiver(models.signals.post_save, sender=LikeFitting)
def populate_fitting_like_cache(sender, instance, **kwargs):
    instance.populate_cache()


@receiver(models.signals.post_delete, sender=LikeFitting)
def remove_fitting_like_cache(sender, instance, **kwargs):
    instance.remove_cache()


class LikeIngredient(models.Model):
    user = models.ForeignKey(User)
    ingredient = models.ForeignKey(Ingredient)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('user', 'ingredient')
        )
        ordering = "-created_at",


class Ask(models.Model):
    ingredient = models.ForeignKey(Ingredient, related_name='asks')
    user = models.ForeignKey(User, related_name='asks')
    content = models.TextField(u'询问内容', null=True, blank=True)
    answered = models.BooleanField(u'是否回答', default=False)

    created_at = models.DateTimeField(u'询问时间', auto_now_add=True)


class FittingForDiscover(models.Model):
    fitting = models.OneToOneField(Fitting, related_name='discover')
    created_at = models.DateTimeField(auto_now_add=True)
