# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class UserProfile(models.Model):
    Gender_Male = u'男'
    Gender_Female = u'女'
    Gender_Secret = u'保密'
    Gender = (
        (Gender_Female, Gender_Female),
        (Gender_Male, Gender_Male),
        (Gender_Secret, Gender_Secret),
    )

    user = models.OneToOneField(User, related_name='profile')
    avatar = models.ImageField(upload_to='avarta', null=True)
    height = models.FloatField(u'身高', default=160)
    gender = models.CharField(u'性别', max_length=8, choices=Gender)
    weight = models.FloatField(u'体重(kg)', default=60)
    bmi = models.FloatField(u'BMI', default=22, db_index=True)


def create_profile(sender, **kw):
    """
    Create the user profile when a user object is created
    """
    user = kw["instance"]
    if kw["created"]:
        profile = UserProfile(user=user)
        profile.save()

post_save.connect(create_profile, sender=User, dispatch_uid="users-profile-creation-signal")


class WeixinAccount(models.Model):
    user = models.OneToOneField(User, related_name='weixin', null=True)
    access_token = models.TextField(null=True, blank=True)
    expires_in = models.DateTimeField(null=True)
    refresh_token = models.TextField(null=True, blank=True)
    union_id = models.CharField(null=True, blank=True, max_length=32, db_index=True, unique=True)
    open_id = models.TextField(null=True, blank=True)

    nickname = models.TextField(null=True, blank=True)
    sex = models.IntegerField(default=0) # 1 for male
    city = models.CharField(max_length=32, null=True, blank=True)
    province = models.CharField(max_length=32, null=True, blank=True)
    country = models.CharField(max_length=32, null=True, blank=True)
    language = models.CharField(max_length=8, null=True, blank=True)
    avatar = models.URLField(null=True)

    def male(self):
        return self.sex == 1

    def __unicode__(self):
        return self.nickname
