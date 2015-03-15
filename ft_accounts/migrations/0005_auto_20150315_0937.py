# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ft_accounts', '0004_auto_20150315_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weixinaccount',
            name='user',
            field=models.OneToOneField(related_name='weixin', null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
