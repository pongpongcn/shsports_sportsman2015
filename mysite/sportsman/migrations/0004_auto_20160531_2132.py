# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0003_student_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='x_jichudaixie',
            field=models.CharField(verbose_name='基础代谢', max_length=255, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='x_jirou',
            field=models.CharField(verbose_name='肌肉', max_length=255, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='x_shuifen',
            field=models.CharField(verbose_name='水分', max_length=255, blank=True, null=True),
        ),
    ]
