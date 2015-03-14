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
