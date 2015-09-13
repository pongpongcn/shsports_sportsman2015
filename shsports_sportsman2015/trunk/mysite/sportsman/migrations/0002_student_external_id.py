# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='external_id',
            field=models.CharField(blank=True, verbose_name='外部标识', max_length=10, null=True),
        ),
    ]
