# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ft_fitting', '0003_auto_20150327_1407'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='likefitting',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='likeingredient',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='like_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
