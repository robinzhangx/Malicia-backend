# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ft_fitting', '0006_remove_ingredient_like_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='picture',
            field=models.ImageField(upload_to=b'ingredients', null=True, verbose_name='\u56fe\u7247'),
            preserve_default=True,
        ),
    ]
