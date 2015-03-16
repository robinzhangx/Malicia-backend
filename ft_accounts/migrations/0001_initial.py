# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('nickname', models.CharField(unique=True, max_length=64, verbose_name=b'nickname')),
                ('email', models.EmailField(unique=True, max_length=75, verbose_name=b'email address')),
                ('avatar', models.ImageField(upload_to=b'avatar', null=True, verbose_name=b'avatar', blank=True)),
                ('description', models.TextField(blank=True)),
                ('height', models.FloatField(default=160, verbose_name='\u8eab\u9ad8')),
                ('gender', models.CharField(max_length=8, verbose_name='\u6027\u522b', choices=[('\u5973', '\u5973'), ('\u7537', '\u7537'), ('\u4fdd\u5bc6', '\u4fdd\u5bc6')])),
                ('weight', models.FloatField(default=60, verbose_name='\u4f53\u91cd(kg)')),
                ('bmi', models.FloatField(default=22, verbose_name='BMI', db_index=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name=b'staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name=b'active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WeixinAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('access_token', models.TextField(null=True, blank=True)),
                ('expires_in', models.DateTimeField(null=True)),
                ('refresh_token', models.TextField(null=True, blank=True)),
                ('union_id', models.CharField(db_index=True, max_length=32, unique=True, null=True, blank=True)),
                ('open_id', models.TextField(null=True, blank=True)),
                ('nickname', models.TextField(null=True, blank=True)),
                ('sex', models.IntegerField(default=0)),
                ('city', models.CharField(max_length=32, null=True, blank=True)),
                ('province', models.CharField(max_length=32, null=True, blank=True)),
                ('country', models.CharField(max_length=32, null=True, blank=True)),
                ('language', models.CharField(max_length=8, null=True, blank=True)),
                ('avatar', models.URLField(null=True)),
                ('user', models.OneToOneField(related_name='weixin', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
