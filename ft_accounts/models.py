# coding=utf-8
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, nickname, email, password,
                    is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, nickname, email, password=None, **extra_fields):
        return self._create_user(nickname, email, password, False, False, **extra_fields)

    def create_superuser(self, nickname, email, password, **extra_fields):
        return self._create_user(nickname, email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    Gender_Male = u'男'
    Gender_Female = u'女'
    Gender_Secret = u'保密'
    Gender = (
        (Gender_Female, Gender_Female),
        (Gender_Male, Gender_Male),
        (Gender_Secret, Gender_Secret),
    )

    nickname = models.CharField('nickname', max_length=64, unique=True)
    email = models.EmailField('email address', unique=True)
    avatar = models.ImageField('avatar', upload_to='avatar', blank=True, null=True)
    description = models.TextField(blank=True)
    height = models.FloatField(u'身高', default=160)
    gender = models.CharField(u'性别', max_length=8, choices=Gender)
    weight = models.FloatField(u'体重(kg)', default=60)
    bmi = models.FloatField(u'BMI', default=22, db_index=True)

    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['email']

    def get_short_name(self):
        return self.nickname

    def get_full_name(self):
        return self.email


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
