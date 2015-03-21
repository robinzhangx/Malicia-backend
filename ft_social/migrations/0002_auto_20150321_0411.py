# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ft_social', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set([('left', 'right')]),
        ),
    ]
