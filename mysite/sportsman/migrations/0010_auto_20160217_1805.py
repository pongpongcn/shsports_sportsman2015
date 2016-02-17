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
            field=models.DecimalField(null=True, verbose_name='测试成绩 20米冲刺跑 第一次（秒）', max_digits=4, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_20m_2',
            field=models.DecimalField(null=True, verbose_name='测试成绩 20米冲刺跑 第二次（秒）', max_digits=4, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal30_1',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='测试成绩 平衡 3.0厘米 第一次（步）', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal30_2',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='测试成绩 平衡 3.0厘米 第二次（步）', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal45_1',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='测试成绩 平衡 4.5厘米 第一次（步）', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal45_2',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='测试成绩 平衡 4.5厘米 第二次（步）', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal60_1',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='测试成绩 平衡 6.0厘米 第一次（步）', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal60_2',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='测试成绩 平衡 6.0厘米 第二次（步）', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_ball_1',
            field=models.DecimalField(null=True, verbose_name='测试成绩 投掷 第一次（米）', max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_ball_2',
            field=models.DecimalField(null=True, verbose_name='测试成绩 投掷 第二次（米）', max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_ball_3',
            field=models.DecimalField(null=True, verbose_name='测试成绩 投掷 第三次（米）', max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_lauf_rest',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='测试成绩 六分跑 最后未完成的一圈所跑距离（米）', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_lauf_runden',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='测试成绩 六分跑 已完成圈数', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_ls',
            field=models.IntegerField(null=True, verbose_name='测试成绩 俯卧撑（重复次数）', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_rb_1',
            field=models.DecimalField(null=True, verbose_name='测试成绩 直身前屈 第一次（厘米）', max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_rb_2',
            field=models.DecimalField(null=True, verbose_name='测试成绩 直身前屈 第二次（厘米）', max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_shh_1f',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='测试成绩 侧向跳 第一次跳（错误次数）', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_shh_1s',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='测试成绩 侧向跳 第一次跳（总次数）', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_shh_2f',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='测试成绩 侧向跳 第二次跳（错误次数）', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_shh_2s',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='测试成绩 侧向跳 第二次跳（总次数）', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_su',
            field=models.IntegerField(null=True, verbose_name='测试成绩 仰卧起坐（重复次数）', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_sws_1',
            field=models.DecimalField(null=True, verbose_name='测试成绩 跳远 第一次（厘米）', max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_sws_2',
            field=models.DecimalField(null=True, verbose_name='测试成绩 跳远 第二次（厘米）', max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='height',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='身高（厘米）', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='weight',
            field=models.DecimalField(null=True, verbose_name='体重（公斤）', max_digits=5, decimal_places=2, blank=True),
        ),
    ]
