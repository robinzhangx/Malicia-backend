# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.ImageField(null=True, upload_to=b'avarta')),
                ('height', models.FloatField(default=160, verbose_name='\u8eab\u9ad8')),
                ('gender', models.CharField(max_length=8, verbose_name='\u6027\u522b', choices=[('\u5973', '\u5973'), ('\u7537', '\u7537'), ('\u4fdd\u5bc6', '\u4fdd\u5bc6')])),
                ('weight', models.FloatField(default=60, verbose_name='\u4f53\u91cd(kg)')),
                ('bmi', models.FloatField(default=22, verbose_name='BMI', db_index=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
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
