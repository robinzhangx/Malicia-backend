# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ft_fitting', '0007_ingredient_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='\u540d\u79f0', db_index=True)),
                ('description', models.TextField(null=True, verbose_name='\u4ecb\u7ecd')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='brand',
            field=models.ForeignKey(to='ft_fitting.Brand', null=True),
            preserve_default=True,
        ),
    ]
