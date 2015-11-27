# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Factor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('gender', models.CharField(verbose_name='性别', choices=[('MALE', '男'), ('FEMALE', '女')], max_length=10)),
                ('month_age', models.IntegerField(verbose_name='月龄')),
                ('movement_type', models.CharField(verbose_name='测试点', choices=[('20m', '20米冲刺跑'), ('bal', '平衡'), ('shh', '侧向跳'), ('rb', '直身前驱'), ('ball', '投掷'), ('ls', '俯卧撑'), ('su', '仰卧起坐'), ('sws', '跳远'), ('lauf', '六分跑'), ('slauf', '星形跑')], max_length=10)),
                ('mean', models.FloatField(verbose_name='平均值')),
                ('standard_deviation', models.FloatField(verbose_name='标准偏差')),
            ],
            options={
                'verbose_name_plural': '分布因素(Factors)',
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='名称', max_length=100)),
                ('universalName', models.CharField(verbose_name='名称（英文）', max_length=100)),
            ],
            options={
                'verbose_name': '学校',
                'verbose_name_plural': '学校',
            },
        ),
        migrations.CreateModel(
            name='SchoolClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='名称', max_length=100)),
                ('universalName', models.CharField(verbose_name='名称（英文）', max_length=100)),
                ('school', models.ForeignKey(verbose_name='学校', to='sportsman.School')),
            ],
            options={
                'verbose_name': '班级',
                'verbose_name_plural': '班级',
            },
        ),
        migrations.CreateModel(
            name='SequenceNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('code', models.CharField(verbose_name='代码', unique=True, max_length=100)),
                ('value', models.BigIntegerField(verbose_name='值（当前）')),
                ('prefix', models.CharField(blank=True, verbose_name='前缀', null=True, max_length=100)),
                ('suffix', models.CharField(blank=True, verbose_name='后缀', null=True, max_length=100)),
            ],
            options={
                'verbose_name': '序列编号',
                'verbose_name_plural': '序列编号',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('noOfStudentStatus', models.CharField(blank=True, verbose_name='学籍号', null=True, max_length=255)),
                ('firstName', models.CharField(verbose_name='名', max_length=255)),
                ('lastName', models.CharField(verbose_name='姓', max_length=255)),
                ('universalFirstName', models.CharField(blank=True, verbose_name='名（英文）', null=True, max_length=255)),
                ('universalLastName', models.CharField(blank=True, verbose_name='姓（英文）', null=True, max_length=255)),
                ('gender', models.CharField(blank=True, verbose_name='性别', null=True, choices=[('MALE', '男'), ('FEMALE', '女')], max_length=255)),
                ('dateOfBirth', models.DateField(blank=True, verbose_name='出生日期', null=True)),
                ('dateOfTesting', models.DateField(blank=True, verbose_name='测试日期', null=True)),
                ('number', models.IntegerField(blank=True, verbose_name='测试编号', null=True)),
                ('questionary', models.IntegerField(blank=True, verbose_name='问卷编号', null=True)),
                ('street', models.CharField(blank=True, verbose_name='路（地址）', null=True, max_length=255)),
                ('housenumber', models.CharField(blank=True, verbose_name='弄（地址）', null=True, max_length=255)),
                ('addition', models.CharField(blank=True, verbose_name='号（地址）', null=True, max_length=255)),
                ('zip', models.CharField(blank=True, verbose_name='邮政编码（地址）', null=True, max_length=255)),
                ('city', models.CharField(blank=True, verbose_name='城市（地址）', null=True, max_length=255)),
                ('addressClearance', models.BooleanField(verbose_name='地址Clearance', default=False)),
                ('e_20m_1', models.DecimalField(blank=True, verbose_name='20米跑 第一次跑（秒）', null=True, max_digits=19, decimal_places=2)),
                ('e_20m_2', models.DecimalField(blank=True, verbose_name='20米跑 第二次跑（秒）', null=True, max_digits=19, decimal_places=2)),
                ('e_bal30_1', models.IntegerField(blank=True, verbose_name='后退平衡 3.0厘米 第一次', null=True)),
                ('e_bal30_2', models.IntegerField(blank=True, verbose_name='后退平衡 3.0厘米 第二次', null=True)),
                ('e_bal45_1', models.IntegerField(blank=True, verbose_name='后退平衡 4.5厘米 第一次', null=True)),
                ('e_bal45_2', models.IntegerField(blank=True, verbose_name='后退平衡 4.5厘米 第二次', null=True)),
                ('e_bal60_1', models.IntegerField(blank=True, verbose_name='后退平衡 6.0厘米 第一次', null=True)),
                ('e_bal60_2', models.IntegerField(blank=True, verbose_name='后退平衡 6.0厘米 第二次', null=True)),
                ('e_ball_1', models.DecimalField(blank=True, verbose_name='投掷球 第一次', null=True, max_digits=19, decimal_places=2)),
                ('e_ball_2', models.DecimalField(blank=True, verbose_name='投掷球 第二次', null=True, max_digits=19, decimal_places=2)),
                ('e_ball_3', models.DecimalField(blank=True, verbose_name='投掷球 第三次', null=True, max_digits=19, decimal_places=2)),
                ('e_lauf_rest', models.IntegerField(blank=True, verbose_name='6分钟跑 最后未完成的一圈所跑距离（米）', null=True)),
                ('e_lauf_runden', models.IntegerField(blank=True, verbose_name='6分钟跑 圈数', null=True)),
                ('e_ls', models.IntegerField(blank=True, verbose_name='俯卧撑 次数（40秒内）', null=True)),
                ('e_rb_1', models.DecimalField(blank=True, verbose_name='立位体前屈 第一次（厘米）', null=True, max_digits=19, decimal_places=2)),
                ('e_rb_2', models.DecimalField(blank=True, verbose_name='立位体前屈 第二次（厘米）', null=True, max_digits=19, decimal_places=2)),
                ('e_shh_1f', models.IntegerField(blank=True, verbose_name='侧向跳 第一次跳（错误次数）', null=True)),
                ('e_shh_1s', models.IntegerField(blank=True, verbose_name='侧向跳 第一次跳（总次数）', null=True)),
                ('e_shh_2f', models.IntegerField(blank=True, verbose_name='侧向跳 第二次跳（错误次数）', null=True)),
                ('e_shh_2s', models.IntegerField(blank=True, verbose_name='侧向跳 第二次跳（总次数）', null=True)),
                ('e_slauf_10', models.DecimalField(blank=True, verbose_name='星形跑重复10次', null=True, max_digits=19, decimal_places=2)),
                ('e_su', models.IntegerField(blank=True, verbose_name='仰卧起坐 次数（40秒内）', null=True)),
                ('e_sws_1', models.DecimalField(blank=True, verbose_name='立定跳远 第一次（厘米）', null=True, max_digits=19, decimal_places=2)),
                ('e_sws_2', models.DecimalField(blank=True, verbose_name='立定跳远 第二次（厘米）', null=True, max_digits=19, decimal_places=2)),
                ('weight', models.DecimalField(blank=True, verbose_name='体重（公斤）', null=True, max_digits=19, decimal_places=2)),
                ('height', models.DecimalField(blank=True, verbose_name='身高（厘米）', null=True, max_digits=19, decimal_places=2)),
                ('last_name', models.CharField(blank=True, verbose_name='姓', null=True, max_length=5)),
                ('first_name', models.CharField(blank=True, verbose_name='名', null=True, max_length=10)),
                ('birth_date', models.DateField(blank=True, verbose_name='出生日期', null=True)),
                ('school_name', models.CharField(blank=True, verbose_name='学校名称', null=True, max_length=100)),
                ('class_name', models.CharField(blank=True, verbose_name='班级名称', null=True, max_length=100)),
                ('external_id', models.CharField(blank=True, verbose_name='外部标识', null=True, max_length=10)),
                ('schoolClass', models.ForeignKey(verbose_name='班级', to='sportsman.SchoolClass')),
            ],
            options={
                'verbose_name': '学生',
                'verbose_name_plural': '学生',
            },
        ),
        migrations.CreateModel(
            name='TestRefData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('movement_type', models.CharField(verbose_name='测试点', choices=[('20m', '20米冲刺跑'), ('bal', '平衡'), ('shh', '侧向跳'), ('rb', '直身前驱'), ('ball', '投掷'), ('ls', '俯卧撑'), ('su', '仰卧起坐'), ('sws', '跳远'), ('lauf', '六分跑'), ('slauf', '星形跑')], max_length=10)),
                ('key', models.CharField(verbose_name='数据项(第一次, 第二次, ...)', max_length=10)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('movement_type', models.CharField(verbose_name='测试点', choices=[('20m', '20米冲刺跑'), ('bal', '平衡'), ('shh', '侧向跳'), ('rb', '直身前驱'), ('ball', '投掷'), ('ls', '俯卧撑'), ('su', '仰卧起坐'), ('sws', '跳远'), ('lauf', '六分跑'), ('slauf', '星形跑')], max_length=10)),
                ('value', models.FloatField(verbose_name='数据值')),
                ('evaluate_date', models.DateTimeField(verbose_name='评估时间')),
                ('evaluate_value', models.FloatField(verbose_name='评估分值')),
                ('test_summary_data', models.ForeignKey(to='sportsman.TestSummaryData')),
            ],
            options={
                'verbose_name_plural': '测试总结单项数据(TestSummaryDataItem)',
            },
        ),
    ]
