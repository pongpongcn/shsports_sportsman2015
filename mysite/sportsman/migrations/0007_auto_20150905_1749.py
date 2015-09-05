# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0006_auto_20150905_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestRefData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('testing_date', models.DateField(verbose_name='测试日期')),
                ('testing_number', models.IntegerField(verbose_name='测试编号')),
            ],
            options={
                'verbose_name_plural': '测试原始记录(TestRefDatas)',
            },
        ),
        migrations.CreateModel(
            name='TestRefDataItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('movement_type', models.CharField(verbose_name='测试点', choices=[('20m', '20米跑'), ('bal', '后退平衡'), ('shh', '侧向跳'), ('rb', '躯体')], max_length=10)),
                ('key', models.CharField(verbose_name='数据项(第一次, 第二次, ...)', max_length=10)),
                ('value', models.FloatField(verbose_name='数据值')),
                ('test_ref_data', models.ForeignKey(to='sportsman.TestRefData')),
            ],
            options={
                'verbose_name_plural': '测试原始记录单项数据(TestRefDataItem)',
            },
        ),
        migrations.CreateModel(
            name='TestSummaryData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('testing_date', models.DateField(verbose_name='测试日期')),
                ('month_age', models.IntegerField(verbose_name='月龄')),
                ('day_age', models.IntegerField(verbose_name='日龄')),
            ],
            options={
                'verbose_name_plural': '测试总结(TestSummaryData)',
            },
        ),
        migrations.CreateModel(
            name='TestSummaryDataItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('movement_type', models.CharField(verbose_name='测试点', choices=[('20m', '20米跑'), ('bal', '后退平衡'), ('shh', '侧向跳'), ('rb', '躯体')], max_length=10)),
                ('value', models.FloatField(verbose_name='数据值')),
                ('probability', models.FloatField(verbose_name='概率')),
            ],
            options={
                'verbose_name_plural': '测试总结单项数据(TestSummaryDataItem)',
            },
        ),
        migrations.AlterModelOptions(
            name='factor',
            options={'verbose_name_plural': '分布因素(Factors)'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name_plural': '学生信息(Students)'},
        ),
        migrations.AddField(
            model_name='testsummarydataitem',
            name='factor',
            field=models.ForeignKey(to='sportsman.Factor'),
        ),
        migrations.AddField(
            model_name='testsummarydataitem',
            name='test_summary_data',
            field=models.ForeignKey(to='sportsman.TestSummaryData'),
        ),
        migrations.AddField(
            model_name='testsummarydata',
            name='student',
            field=models.ForeignKey(to='sportsman.Student'),
        ),
        migrations.AddField(
            model_name='testsummarydata',
            name='test_ref_data',
            field=models.ForeignKey(to='sportsman.TestRefData'),
        ),
        migrations.AddField(
            model_name='testrefdata',
            name='student',
            field=models.ForeignKey(to='sportsman.Student'),
        ),
    ]
