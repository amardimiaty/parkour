# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-15 12:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index_generator', '0004_poolsize'),
    ]

    operations = [
        migrations.AddField(
            model_name='pool',
            name='size',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='index_generator.PoolSize', verbose_name='Size'),
            preserve_default=False,
        ),
    ]
