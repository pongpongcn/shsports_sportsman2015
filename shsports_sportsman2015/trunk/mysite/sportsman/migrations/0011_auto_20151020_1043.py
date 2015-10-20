# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0010_auto_20151020_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencenumber',
            name='prefix',
            field=models.CharField(verbose_name='前缀', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='sequencenumber',
            name='suffix',
            field=models.CharField(verbose_name='后缀', max_length=100, null=True, blank=True),
        ),
    ]
