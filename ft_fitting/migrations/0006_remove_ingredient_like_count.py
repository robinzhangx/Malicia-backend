# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ft_fitting', '0005_remove_fitting_like_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='like_count',
        ),
    ]
