# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0009_auto_20151017_1419'),
    ]

    operations = [
        migrations.CreateModel(
            name='SequenceNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, verbose_name='代码')),
                ('value', models.BigIntegerField(verbose_name='值（当前）')),
                ('prefix', models.CharField(max_length=100, verbose_name='前缀')),
                ('suffix', models.CharField(max_length=100, verbose_name='后缀')),
            ],
            options={
                'verbose_name_plural': '序列编号',
                'verbose_name': '序列编号',
            },
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name_plural': '学生', 'verbose_name': '学生'},
        ),
        migrations.AlterField(
            model_name='student',
            name='dateOfTesting',
            field=models.DateField(null=True, blank=True, verbose_name='考试日期'),
        ),
    ]
