# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ft_fitting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FittingForDiscover',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('fitting', models.OneToOneField(related_name='discover', to='ft_fitting.Fitting')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
