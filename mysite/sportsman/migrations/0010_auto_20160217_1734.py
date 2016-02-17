# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0009_auto_20160126_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='e_20m_1',
            field=models.DecimalField(blank=True, max_digits=4, verbose_name='测试成绩 20米跑 第一次（秒）', decimal_places=2, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_20m_2',
            field=models.DecimalField(blank=True, max_digits=4, verbose_name='测试成绩 20米跑 第二次（秒）', decimal_places=2, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal30_1',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='测试成绩 后退平衡 3.0厘米 第一次（次数）', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal30_2',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='测试成绩 后退平衡 3.0厘米 第二次（次数）', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal45_1',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='测试成绩 后退平衡 4.5厘米 第一次（次数）', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal45_2',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='测试成绩 后退平衡 4.5厘米 第二次（次数）', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal60_1',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='测试成绩 后退平衡 6.0厘米 第一次（次数）', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal60_2',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='测试成绩 后退平衡 6.0厘米 第二次（次数）', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_ball_1',
            field=models.DecimalField(blank=True, max_digits=5, verbose_name='测试成绩 投掷球 第一次（米）', decimal_places=2, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_ball_2',
            field=models.DecimalField(blank=True, max_digits=5, verbose_name='测试成绩 投掷球 第二次（米）', decimal_places=2, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_ball_3',
            field=models.DecimalField(blank=True, max_digits=5, verbose_name='测试成绩 投掷球 第三次（米）', decimal_places=2, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_lauf_rest',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='测试成绩 6分钟跑 最后未完成的一圈所跑距离（米）', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_lauf_runden',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='测试成绩 6分钟跑 圈数', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_ls',
            field=models.IntegerField(blank=True, verbose_name='测试成绩 俯卧撑（次数）', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_rb_1',
            field=models.DecimalField(blank=True, max_digits=5, verbose_name='测试成绩 立位体前屈 第一次（厘米）', decimal_places=2, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_rb_2',
            field=models.DecimalField(blank=True, max_digits=5, verbose_name='测试成绩 立位体前屈 第二次（厘米）', decimal_places=2, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_shh_1f',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='测试成绩 侧向跳 第一次跳（错误次数）', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_shh_1s',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='测试成绩 侧向跳 第一次跳（总次数）', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_shh_2f',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='测试成绩 侧向跳 第二次跳（错误次数）', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_shh_2s',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='测试成绩 侧向跳 第二次跳（总次数）', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_su',
            field=models.IntegerField(blank=True, verbose_name='测试成绩 仰卧起坐（次数）', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_sws_1',
            field=models.DecimalField(blank=True, max_digits=5, verbose_name='测试成绩 立定跳远 第一次（厘米）', decimal_places=2, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_sws_2',
            field=models.DecimalField(blank=True, max_digits=5, verbose_name='测试成绩 立定跳远 第二次（厘米）', decimal_places=2, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='height',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='身高（厘米）', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='weight',
            field=models.DecimalField(blank=True, max_digits=5, verbose_name='体重（公斤）', decimal_places=2, null=True),
        ),
    ]
