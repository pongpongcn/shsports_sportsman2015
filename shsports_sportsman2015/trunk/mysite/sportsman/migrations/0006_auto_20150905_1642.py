# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0005_auto_20150905_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='dateOfBirth',
            field=models.DateField(verbose_name='出生日期'),
        ),
    ]
