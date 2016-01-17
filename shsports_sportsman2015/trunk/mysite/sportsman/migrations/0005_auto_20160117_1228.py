# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0004_auto_20160117_1110'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='factor',
            options={'verbose_name_plural': '分布因素', 'verbose_name': '分布因素'},
        ),
        migrations.RemoveField(
            model_name='factor',
            name='mean',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='movement_type',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='standard_deviation',
        ),
        migrations.AddField(
            model_name='factor',
            name='mean_20m',
            field=models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='20米跑平均值'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='mean_bal',
            field=models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='后退平衡平均值'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='mean_ball',
            field=models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='投掷球平均值'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='mean_lauf',
            field=models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='6分钟跑平均值'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='mean_ls',
            field=models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='俯卧撑平均值'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='mean_rb',
            field=models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='立位体前屈平均值'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='mean_shh',
            field=models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='侧向跳平均值'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='mean_su',
            field=models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='仰卧起坐平均值'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='mean_sws',
            field=models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='立定跳远平均值'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='standard_deviation_20m',
            field=models.DecimalField(decimal_places=4, max_digits=10, default=0, verbose_name='20米跑标准偏差'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='standard_deviation_bal',
            field=models.DecimalField(decimal_places=4, max_digits=10, default=0, verbose_name='后退平衡标准偏差'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='standard_deviation_ball',
            field=models.DecimalField(decimal_places=4, max_digits=10, default=0, verbose_name='投掷球标准偏差'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='standard_deviation_lauf',
            field=models.DecimalField(decimal_places=4, max_digits=10, default=0, verbose_name='6分钟跑标准偏差'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='standard_deviation_ls',
            field=models.DecimalField(decimal_places=4, max_digits=10, default=0, verbose_name='俯卧撑标准偏差'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='standard_deviation_rb',
            field=models.DecimalField(decimal_places=4, max_digits=10, default=0, verbose_name='立位体前屈标准偏差'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='standard_deviation_shh',
            field=models.DecimalField(decimal_places=4, max_digits=10, default=0, verbose_name='侧向跳标准偏差'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='standard_deviation_su',
            field=models.DecimalField(decimal_places=4, max_digits=10, default=0, verbose_name='仰卧起坐标准偏差'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='standard_deviation_sws',
            field=models.DecimalField(decimal_places=4, max_digits=10, default=0, verbose_name='立定跳远标准偏差'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='version',
            field=models.CharField(verbose_name='版本', max_length=100, default='obsolete'),
            preserve_default=False,
        ),
    ]
