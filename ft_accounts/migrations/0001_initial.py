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
                ('nickname', models.CharField(unique=True, max_length=128, verbose_name='\u6635\u79f0', db_index=True)),
                ('height', models.FloatField(default=160, verbose_name='\u8eab\u9ad8')),
                ('gender', models.CharField(max_length=8, verbose_name='\u6027\u522b', choices=[('\u5973', '\u5973'), ('\u7537', '\u7537'), ('\u4fdd\u5bc6', '\u4fdd\u5bc6')])),
                ('weight', models.FloatField(default=60, verbose_name='\u4f53\u91cd(kg)')),
                ('bmi', models.FloatField(default=22, verbose_name='BMI', db_index=True)),
                ('user', models.ForeignKey(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
