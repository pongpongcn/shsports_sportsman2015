# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0012_auto_20160221_1125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentevaluation',
            name='certificate_template',
        ),
        migrations.AlterField(
            model_name='studentevaluation',
            name='certificate_data',
            field=models.TextField(null=True, blank=True, verbose_name='证书数据'),
        ),
    ]
