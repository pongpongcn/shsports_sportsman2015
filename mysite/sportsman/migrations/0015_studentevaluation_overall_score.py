# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0014_auto_20160305_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentevaluation',
            name='overall_score',
            field=models.PositiveSmallIntegerField(verbose_name='总分', null=True, blank=True),
        ),
    ]
