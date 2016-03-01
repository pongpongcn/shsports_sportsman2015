# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0011_auto_20160222_0321'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestPlan',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('startDate', models.DateField(blank=True, null=True, verbose_name='开始日期')),
                ('endDate', models.DateField(blank=True, null=True, verbose_name='结束日期')),
                ('isPublished', models.BooleanField(verbose_name='已发布', default=False)),
            ],
            options={
                'verbose_name': '测试批次',
                'verbose_name_plural': '测试批次',
            },
        ),
        migrations.AddField(
            model_name='student',
            name='testPlan',
            field=models.ForeignKey(to='sportsman.TestPlan', blank=True, verbose_name='测试批次', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='testPlan',
            field=models.ForeignKey(to='sportsman.TestPlan', blank=True, verbose_name='测试批次', null=True),
        ),
    ]
