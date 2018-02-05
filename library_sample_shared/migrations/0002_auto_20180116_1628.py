# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-16 15:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library_sample_shared', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexPair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordinate', models.CharField(max_length=5)),
            ],
            options={
                'verbose_name': 'Index Pair',
                'verbose_name_plural': 'Index Pairs',
            },
        ),
        migrations.RemoveField(
            model_name='indextype',
            name='is_index_i5',
        ),
        migrations.RemoveField(
            model_name='indextype',
            name='is_index_i7',
        ),
        migrations.AddField(
            model_name='indexi5',
            name='number',
            field=models.CharField(default='', max_length=10, verbose_name='Number'),
        ),
        migrations.AddField(
            model_name='indexi5',
            name='prefix',
            field=models.CharField(default='', max_length=10, verbose_name='Prefix'),
        ),
        migrations.AddField(
            model_name='indexi7',
            name='number',
            field=models.CharField(default='', max_length=10, verbose_name='Number'),
        ),
        migrations.AddField(
            model_name='indexi7',
            name='prefix',
            field=models.CharField(default='', max_length=10, verbose_name='Prefix'),
        ),
        migrations.AddField(
            model_name='indextype',
            name='format',
            field=models.CharField(choices=[('single', 'single tube'), ('plate', 'plate')], default='single', max_length=11, verbose_name='Format'),
        ),
        migrations.AddField(
            model_name='indextype',
            name='is_dual',
            field=models.BooleanField(default=False, verbose_name='Is Dual'),
        ),
        migrations.AlterField(
            model_name='indexi5',
            name='index_id',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Index ID'),
        ),
        migrations.AlterField(
            model_name='indexi7',
            name='index_id',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Index ID'),
        ),
        migrations.AddField(
            model_name='indexpair',
            name='index1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_sample_shared.IndexI7', verbose_name='Index 1'),
        ),
        migrations.AddField(
            model_name='indexpair',
            name='index2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library_sample_shared.IndexI5', verbose_name='Index 2'),
        ),
        migrations.AddField(
            model_name='indexpair',
            name='index_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_sample_shared.IndexType', verbose_name='Index Type'),
        ),
    ]
