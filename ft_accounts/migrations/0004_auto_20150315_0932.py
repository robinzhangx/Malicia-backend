# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ft_accounts', '0003_remove_userprofile_nickname'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeixinAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('access_token', models.TextField(null=True, blank=True)),
                ('expires_in', models.DateTimeField(null=True)),
                ('refresh_token', models.TextField(null=True, blank=True)),
                ('union_id', models.TextField(db_index=True, unique=True, null=True, blank=True)),
                ('open_id', models.TextField(null=True, blank=True)),
                ('nickname', models.TextField(null=True, blank=True)),
                ('sex', models.IntegerField(default=0)),
                ('city', models.CharField(max_length=32, null=True, blank=True)),
                ('province', models.CharField(max_length=32, null=True, blank=True)),
                ('country', models.CharField(max_length=32, null=True, blank=True)),
                ('language', models.CharField(max_length=8, null=True, blank=True)),
                ('avatar', models.URLField(null=True)),
                ('user', models.OneToOneField(related_name='weixin', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(null=True, upload_to=b'avarta'),
            preserve_default=True,
        ),
    ]
