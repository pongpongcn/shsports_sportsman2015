# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0013_student_noofstudentstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='birth_date',
            field=models.DateField(null=True, blank=True, verbose_name='出生日期'),
        ),
        migrations.AlterField(
            model_name='student',
            name='class_name',
            field=models.CharField(null=True, blank=True, max_length=100, verbose_name='班级名称'),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(null=True, blank=True, max_length=10, verbose_name='名'),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(null=True, blank=True, max_length=5, verbose_name='姓'),
        ),
        migrations.AlterField(
            model_name='student',
            name='school_name',
            field=models.CharField(null=True, blank=True, max_length=100, verbose_name='学校名称'),
        ),
    ]
