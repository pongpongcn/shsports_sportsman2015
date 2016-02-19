# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0012_auto_20160220_0117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentevaluation',
            name='age',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='bmi',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='day_age',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='month_age',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='score_sum',
        ),
        migrations.AlterField(
            model_name='studentevaluation',
            name='certificate',
            field=models.FileField(verbose_name='证书', null=True, blank=True, upload_to='certificates/%Y/%m/%d/'),
        ),
    ]
