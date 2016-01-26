# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0008_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentEvaluation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('month_age', models.IntegerField(verbose_name='月龄')),
                ('day_age', models.IntegerField(verbose_name='日龄')),
                ('bmi', models.DecimalField(verbose_name='BMI', max_digits=3, decimal_places=1)),
                ('original_score_bal', models.IntegerField(verbose_name='后退平衡 原始成绩')),
                ('percentage_bal', models.DecimalField(verbose_name='后退平衡 评价', max_digits=5, decimal_places=2)),
                ('original_score_shh', models.DecimalField(verbose_name='侧向跳 原始成绩', max_digits=19, decimal_places=2)),
                ('percentage_shh', models.DecimalField(verbose_name='侧向跳 评价', max_digits=5, decimal_places=2)),
                ('original_score_sws', models.DecimalField(verbose_name='立定跳远 原始成绩', max_digits=19, decimal_places=2)),
                ('percentage_sws', models.DecimalField(verbose_name='立定跳远 评价', max_digits=5, decimal_places=2)),
                ('original_score_20m', models.DecimalField(verbose_name='20米跑 原始成绩', max_digits=19, decimal_places=2)),
                ('percentage_20m', models.DecimalField(verbose_name='20米跑 评价', max_digits=5, decimal_places=2)),
                ('original_score_su', models.IntegerField(verbose_name='仰卧起坐 原始成绩')),
                ('percentage_su', models.DecimalField(verbose_name='仰卧起坐 评价', max_digits=5, decimal_places=2)),
                ('original_score_ls', models.IntegerField(verbose_name='俯卧撑 原始成绩')),
                ('percentage_ls', models.DecimalField(verbose_name='俯卧撑 评价', max_digits=5, decimal_places=2)),
                ('original_score_rb', models.DecimalField(verbose_name='立位体前屈 原始成绩', max_digits=19, decimal_places=2)),
                ('percentage_rb', models.DecimalField(verbose_name='立位体前屈 评价', max_digits=5, decimal_places=2)),
                ('original_score_lauf', models.IntegerField(verbose_name='6分钟跑 原始成绩')),
                ('percentage_lauf', models.DecimalField(verbose_name='6分钟跑 评价', max_digits=5, decimal_places=2)),
                ('original_score_ball', models.DecimalField(verbose_name='投掷球 原始成绩', max_digits=19, decimal_places=2)),
                ('percentage_ball', models.DecimalField(verbose_name='投掷球 评价', max_digits=5, decimal_places=2)),
                ('score_sum', models.DecimalField(verbose_name='评价总分', max_digits=19, decimal_places=2)),
                ('student', models.OneToOneField(to='sportsman.Student')),
            ],
            options={
                'verbose_name': '学生评价',
                'verbose_name_plural': '学生评价',
            },
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': '用户资料', 'verbose_name_plural': '用户资料'},
        ),
    ]
