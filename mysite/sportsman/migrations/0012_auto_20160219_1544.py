# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0011_auto_20160219_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentevaluation',
            name='e_20m',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='e_bal',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='e_ball',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='e_lauf',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='e_ls',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='e_rb',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='e_shh',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='e_su',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='e_sws',
        ),
    ]
