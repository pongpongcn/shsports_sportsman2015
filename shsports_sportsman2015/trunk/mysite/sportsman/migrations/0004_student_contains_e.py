# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0003_auto_20161121_0005'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='contains_e',
            field=models.IntegerField(null=True, verbose_name='表明是否有成绩数据, 以便更好的处理评价.', blank=True),
        ),
    ]
