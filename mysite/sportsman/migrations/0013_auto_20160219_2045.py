# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0012_auto_20160219_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentevaluation',
            name='p_bmi',
            field=models.PositiveSmallIntegerField(verbose_name='百分等级 BMI', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_height',
            field=models.PositiveSmallIntegerField(verbose_name='百分等级 身高', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_weight',
            field=models.PositiveSmallIntegerField(verbose_name='百分等级 体重', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentevaluation',
            name='p_20m',
            field=models.PositiveSmallIntegerField(verbose_name='百分等级 20米冲刺跑', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentevaluation',
            name='p_bal',
            field=models.PositiveSmallIntegerField(verbose_name='百分等级 平衡', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentevaluation',
            name='p_ball',
            field=models.PositiveSmallIntegerField(verbose_name='百分等级 投掷', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentevaluation',
            name='p_lauf',
            field=models.PositiveSmallIntegerField(verbose_name='百分等级 六分跑', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentevaluation',
            name='p_ls',
            field=models.PositiveSmallIntegerField(verbose_name='百分等级 俯卧撑', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentevaluation',
            name='p_rb',
            field=models.PositiveSmallIntegerField(verbose_name='百分等级 直身前屈', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentevaluation',
            name='p_shh',
            field=models.PositiveSmallIntegerField(verbose_name='百分等级 侧向跳', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentevaluation',
            name='p_su',
            field=models.PositiveSmallIntegerField(verbose_name='百分等级 仰卧起坐', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentevaluation',
            name='p_sws',
            field=models.PositiveSmallIntegerField(verbose_name='百分等级 跳远', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentevaluation',
            name='score_sum',
            field=models.DecimalField(decimal_places=2, verbose_name='总分', max_digits=19),
        ),
    ]
