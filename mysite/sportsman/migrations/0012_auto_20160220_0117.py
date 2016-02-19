# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0011_auto_20160220_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentevaluation',
            name='certificate',
            field=models.FileField(upload_to='certificates/%Y/%m/%d/', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='is_frail',
            field=models.BooleanField(verbose_name='需要运动健康干预', default=False),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='is_talent',
            field=models.BooleanField(verbose_name='运动天才', default=False),
        ),
    ]
