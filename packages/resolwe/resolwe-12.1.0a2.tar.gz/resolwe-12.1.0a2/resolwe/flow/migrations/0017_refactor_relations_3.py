# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-06 02:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0016_refactor_relations_2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relationpartition',
            name='position',
        ),
        migrations.AddField(
            model_name='relationpartition',
            name='position',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, null=True),
        ),
    ]
