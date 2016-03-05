# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0013_auto_20160304_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentevaluation',
            name='frail_rank_number',
            field=models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='需要健康干预排名'),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='talent_rank_number',
            field=models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='运动天赋优秀排名'),
        ),
    ]
