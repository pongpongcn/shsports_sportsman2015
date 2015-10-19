# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0005_auto_20151017_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(verbose_name='名称', max_length=100),
        ),
        migrations.AlterField(
            model_name='schoolclass',
            name='name',
            field=models.CharField(verbose_name='名称', max_length=100),
        ),
    ]
