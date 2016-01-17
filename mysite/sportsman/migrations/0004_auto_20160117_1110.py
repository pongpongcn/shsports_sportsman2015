# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0003_standardparameter'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='standardparameter',
            options={'verbose_name_plural': '标准值表', 'verbose_name': '标准值表'},
        ),
        migrations.AddField(
            model_name='standardparameter',
            name='version',
            field=models.CharField(max_length=100, default='for_china_by_german_at_201510', verbose_name='版本'),
            preserve_default=False,
        ),
    ]
