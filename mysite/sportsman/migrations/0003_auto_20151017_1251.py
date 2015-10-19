# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0002_student_external_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testsummarydataitem',
            name='evaluate_date',
            field=models.DateTimeField(verbose_name='评估时间'),
        ),
        migrations.AlterField(
            model_name='testsummarydataitem',
            name='evaluate_value',
            field=models.FloatField(verbose_name='评估分值'),
        ),
    ]
