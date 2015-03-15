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
            name='Ask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(null=True, verbose_name='\u8be2\u95ee\u5185\u5bb9', blank=True)),
                ('answered', models.BooleanField(default=False, verbose_name='\u662f\u5426\u56de\u7b54')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u8be2\u95ee\u65f6\u95f4')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fitting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bmi', models.FloatField(default=22, verbose_name='\u5f53\u65f6\u7684BMI')),
                ('title', models.CharField(max_length=256, verbose_name='\u9898\u76ee')),
                ('picture', models.ImageField(upload_to=b'fitting', verbose_name='\u56fe\u7247')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('like_count', models.IntegerField(default=0, verbose_name='\u559c\u7231')),
                ('user', models.ForeignKey(related_name='fittings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('part', models.CharField(choices=[('\u4e0a\u88c5', '\u4e0a\u88c5'), ('\u4e0b\u88c5', '\u4e0b\u88c5'), ('\u978b', '\u978b'), ('\u5305', '\u5305'), ('\u914d\u4ef6', '\u914d\u4ef6')], max_length=32, blank=True, null=True, verbose_name='\u90e8\u4ef6\u540d\u79f0', db_index=True)),
                ('size', models.CharField(max_length=32, null=True, verbose_name='\u5c3a\u7801', blank=True)),
                ('like_count', models.IntegerField(default=0, verbose_name='\u559c\u7231\u6570')),
                ('fittings', models.ManyToManyField(related_name='ingredients', to='ft_fitting.Fitting')),
                ('user', models.ForeignKey(related_name='ingredients', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ask',
            name='ingredient',
            field=models.ForeignKey(related_name='asks', to='ft_fitting.Ingredient'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ask',
            name='user',
            field=models.ForeignKey(related_name='asks', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
