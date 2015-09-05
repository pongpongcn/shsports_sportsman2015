# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0002_auto_20150905_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='gender',
            field=models.CharField(max_length=10, verbose_name='性别', null=True, choices=[('MALE', '男'), ('FEMALE', '女')]),
        ),
        migrations.AlterField(
            model_name='factor',
            name='month_age',
            field=models.IntegerField(verbose_name='月龄'),
        ),
        migrations.AlterField(
            model_name='factor',
            name='movement_type',
            field=models.CharField(max_length=10, verbose_name='测试点', null=True, choices=[('20m', '20米跑'), ('bal', '后退平衡'), ('shh', '侧向跳'), ('rb', '躯体')]),
        ),
    ]
