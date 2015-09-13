# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Factor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('gender', models.CharField(verbose_name='性别', max_length=10, choices=[('MALE', '男'), ('FEMALE', '女')])),
                ('month_age', models.IntegerField(verbose_name='月龄')),
                ('movement_type', models.CharField(verbose_name='测试点', max_length=10, choices=[('20m', '20米冲刺跑'), ('bal', '平衡'), ('shh', '侧向跳'), ('rb', '直身前驱'), ('ball', '投掷'), ('ls', '俯卧撑'), ('su', '仰卧起坐'), ('sws', '跳远'), ('lauf', '六分跑')])),
                ('mean', models.FloatField(verbose_name='平均值')),
                ('standard_deviation', models.FloatField(verbose_name='标准偏差')),
            ],
            options={
                'verbose_name_plural': '分布因素(Factors)',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('last_name', models.CharField(max_length=5, verbose_name='姓')),
                ('first_name', models.CharField(max_length=10, verbose_name='名')),
                ('gender', models.CharField(verbose_name='性别', max_length=10, choices=[('MALE', '男'), ('FEMALE', '女')])),
                ('birth_date', models.DateField(verbose_name='出生日期')),
                ('school_name', models.CharField(max_length=100, verbose_name='学校名称')),
                ('class_name', models.CharField(max_length=100, verbose_name='班级名称')),
            ],
            options={
                'verbose_name_plural': '学生信息(Students)',
            },
        ),
        migrations.CreateModel(
            name='TestRefData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('testing_date', models.DateField(verbose_name='测试日期')),
                ('testing_number', models.IntegerField(verbose_name='测试编号')),
                ('height', models.FloatField(verbose_name='身高')),
                ('weight', models.FloatField(verbose_name='体重')),
                ('student', models.ForeignKey(verbose_name='测试学生', to='sportsman.Student')),
            ],
            options={
                'verbose_name_plural': '测试原始记录(TestRefDatas)',
            },
        ),
        migrations.CreateModel(
            name='TestRefDataItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('movement_type', models.CharField(verbose_name='测试点', max_length=10, choices=[('20m', '20米冲刺跑'), ('bal', '平衡'), ('shh', '侧向跳'), ('rb', '直身前驱'), ('ball', '投掷'), ('ls', '俯卧撑'), ('su', '仰卧起坐'), ('sws', '跳远'), ('lauf', '六分跑')])),
                ('key', models.CharField(max_length=10, verbose_name='数据项(第一次, 第二次, ...)')),
                ('value', models.FloatField(verbose_name='数据值')),
                ('test_ref_data', models.ForeignKey(verbose_name='测试原始记录', to='sportsman.TestRefData')),
            ],
            options={
                'verbose_name_plural': '测试原始记录单项数据(TestRefDataItem)',
            },
        ),
        migrations.CreateModel(
            name='TestSummaryData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('testing_date', models.DateField(verbose_name='测试日期')),
                ('height', models.FloatField(verbose_name='身高')),
                ('weight', models.FloatField(verbose_name='体重')),
                ('month_age', models.IntegerField(verbose_name='月龄')),
                ('day_age', models.IntegerField(verbose_name='日龄')),
                ('student', models.ForeignKey(to='sportsman.Student')),
                ('test_ref_data', models.ForeignKey(to='sportsman.TestRefData')),
            ],
            options={
                'verbose_name_plural': '测试总结(TestSummaryData)',
            },
        ),
        migrations.CreateModel(
            name='TestSummaryDataItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('movement_type', models.CharField(verbose_name='测试点', max_length=10, choices=[('20m', '20米冲刺跑'), ('bal', '平衡'), ('shh', '侧向跳'), ('rb', '直身前驱'), ('ball', '投掷'), ('ls', '俯卧撑'), ('su', '仰卧起坐'), ('sws', '跳远'), ('lauf', '六分跑')])),
                ('value', models.FloatField(verbose_name='数据值')),
                ('evaluate_date', models.DateTimeField(verbose_name='测试日期')),
                ('evaluate_value', models.FloatField(verbose_name='概率')),
                ('test_summary_data', models.ForeignKey(to='sportsman.TestSummaryData')),
            ],
            options={
                'verbose_name_plural': '测试总结单项数据(TestSummaryDataItem)',
            },
        ),
    ]
