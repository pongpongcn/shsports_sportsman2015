# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0014_auto_20151027_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='dateOfTesting',
            field=models.DateField(blank=True, null=True, verbose_name='测试日期'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_20m_1',
            field=models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=19, verbose_name='20米跑 第一次跑（秒）'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_20m_2',
            field=models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=19, verbose_name='20米跑 第二次跑（秒）'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal30_1',
            field=models.IntegerField(blank=True, null=True, verbose_name='后退平衡 3.0厘米 第一次'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal30_2',
            field=models.IntegerField(blank=True, null=True, verbose_name='后退平衡 3.0厘米 第二次'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal45_1',
            field=models.IntegerField(blank=True, null=True, verbose_name='后退平衡 4.5厘米 第一次'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal45_2',
            field=models.IntegerField(blank=True, null=True, verbose_name='后退平衡 4.5厘米 第二次'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal60_1',
            field=models.IntegerField(blank=True, null=True, verbose_name='后退平衡 6.0厘米 第一次'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_bal60_2',
            field=models.IntegerField(blank=True, null=True, verbose_name='后退平衡 6.0厘米 第二次'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_ball_1',
            field=models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=19, verbose_name='投掷球 第一次'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_ball_2',
            field=models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=19, verbose_name='投掷球 第二次'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_ball_3',
            field=models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=19, verbose_name='投掷球 第三次'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_lauf_rest',
            field=models.IntegerField(blank=True, null=True, verbose_name='6分钟跑 最后未完成的一圈所跑距离（米）'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_lauf_runden',
            field=models.IntegerField(blank=True, null=True, verbose_name='6分钟跑 圈数'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_ls',
            field=models.IntegerField(blank=True, null=True, verbose_name='俯卧撑 次数（40秒内）'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_rb_1',
            field=models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=19, verbose_name='立位体前屈 第一次（厘米）'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_rb_2',
            field=models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=19, verbose_name='立位体前屈 第二次（厘米）'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_shh_1f',
            field=models.IntegerField(blank=True, null=True, verbose_name='侧向跳 第一次跳（错误次数）'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_shh_1s',
            field=models.IntegerField(blank=True, null=True, verbose_name='侧向跳 第一次跳（总次数）'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_shh_2f',
            field=models.IntegerField(blank=True, null=True, verbose_name='侧向跳 第二次跳（错误次数）'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_shh_2s',
            field=models.IntegerField(blank=True, null=True, verbose_name='侧向跳 第二次跳（总次数）'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_su',
            field=models.IntegerField(blank=True, null=True, verbose_name='仰卧起坐 次数（40秒内）'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_sws_1',
            field=models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=19, verbose_name='立定跳远 第一次（厘米）'),
        ),
        migrations.AlterField(
            model_name='student',
            name='e_sws_2',
            field=models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=19, verbose_name='立定跳远 第二次（厘米）'),
        ),
        migrations.AlterField(
            model_name='student',
            name='number',
            field=models.IntegerField(blank=True, null=True, verbose_name='测试编号'),
        ),
        migrations.AlterField(
            model_name='student',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=19, verbose_name='体重（公斤）'),
        ),
    ]
