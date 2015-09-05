# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0003_auto_20150905_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='mean',
            field=models.FloatField(verbose_name='平均值', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='standard_deviation',
            field=models.FloatField(verbose_name='标准偏差', default=0),
            preserve_default=False,
        ),
    ]
