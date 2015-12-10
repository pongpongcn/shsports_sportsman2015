# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='height',
            field=models.IntegerField(null=True, blank=True, verbose_name='身高（厘米）'),
        ),
    ]
