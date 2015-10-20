# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0011_auto_20151020_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencenumber',
            name='code',
            field=models.CharField(verbose_name='代码', max_length=100, unique=True),
        ),
    ]
