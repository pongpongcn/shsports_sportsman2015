# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0008_auto_20151017_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='addressClearance',
            field=models.BooleanField(default=False, verbose_name='地址Clearance'),
        ),
        migrations.AlterField(
            model_name='student',
            name='dateOfBirth',
            field=models.DateField(null=True, blank=True, verbose_name='出生日期'),
        ),
        migrations.AlterField(
            model_name='student',
            name='dateOfTesting',
            field=models.DateField(null=True, blank=True, verbose_name='测试日期'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_20m_1',
            field=models.DecimalField(null=True, max_digits=19, decimal_places=2, blank=True, verbose_name='20米冲刺跑1'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_20m_2',
            field=models.DecimalField(null=True, max_digits=19, decimal_places=2, blank=True, verbose_name='20米冲刺跑2'),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(null=True, max_length=255, blank=True, choices=[('MALE', '男'), ('FEMALE', '女')], verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='student',
            name='number',
            field=models.IntegerField(null=True, blank=True, verbose_name='测试号码'),
        ),
        migrations.AlterField(
            model_name='student',
            name='questionary',
            field=models.IntegerField(null=True, blank=True, verbose_name='问卷编号'),
        ),
    ]
