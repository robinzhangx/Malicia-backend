# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ft_fitting', '0004_auto_20150327_1546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fitting',
            name='like_count',
        ),
    ]
