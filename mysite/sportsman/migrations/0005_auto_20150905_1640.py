# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0004_auto_20150905_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('last_name', models.CharField(max_length=5, verbose_name='姓')),
                ('first_name', models.CharField(max_length=10, verbose_name='名')),
                ('gender', models.CharField(choices=[('MALE', '男'), ('FEMALE', '女')], verbose_name='性别', max_length=10)),
                ('dateOfBirth', models.DateTimeField(verbose_name='出生日期')),
                ('schoolName', models.CharField(max_length=100, verbose_name='学校名称')),
                ('className', models.CharField(max_length=100, verbose_name='班级名称')),
                ('height', models.FloatField(verbose_name='身高')),
                ('weight', models.FloatField(verbose_name='体重')),
            ],
        ),
        migrations.AlterField(
            model_name='factor',
            name='gender',
            field=models.CharField(default='MALE', choices=[('MALE', '男'), ('FEMALE', '女')], verbose_name='性别', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='factor',
            name='movement_type',
            field=models.CharField(default='20m', choices=[('20m', '20米跑'), ('bal', '后退平衡'), ('shh', '侧向跳'), ('rb', '躯体')], verbose_name='测试点', max_length=10),
            preserve_default=False,
        ),
    ]
