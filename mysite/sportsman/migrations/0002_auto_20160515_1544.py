# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('code', models.CharField(unique=True, max_length=50, verbose_name='代码')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('universalName', models.CharField(max_length=50, verbose_name='名称（英文）')),
            ],
            options={
                'verbose_name': '体育项目',
                'verbose_name_plural': '体育项目',
            },
        ),
        migrations.CreateModel(
            name='SportPotentialFactor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('weight_p_bal', models.DecimalField(max_digits=6, verbose_name='权重 平衡', decimal_places=4)),
                ('weight_p_shh', models.DecimalField(max_digits=6, verbose_name='权重 侧向跳', decimal_places=4)),
                ('weight_p_sws', models.DecimalField(max_digits=6, verbose_name='权重 跳远', decimal_places=4)),
                ('weight_p_20m', models.DecimalField(max_digits=6, verbose_name='权重 20米冲刺跑', decimal_places=4)),
                ('weight_p_su', models.DecimalField(max_digits=6, verbose_name='权重 仰卧起坐', decimal_places=4)),
                ('weight_p_ls', models.DecimalField(max_digits=6, verbose_name='权重 俯卧撑', decimal_places=4)),
                ('weight_p_rb', models.DecimalField(max_digits=6, verbose_name='权重 直身前屈', decimal_places=4)),
                ('weight_p_lauf', models.DecimalField(max_digits=6, verbose_name='权重 六分跑', decimal_places=4)),
                ('weight_p_ball', models.DecimalField(max_digits=6, verbose_name='权重 投掷', decimal_places=4)),
                ('weight_p_height', models.DecimalField(max_digits=6, verbose_name='权重 身高', decimal_places=4)),
                ('weight_p_weight', models.DecimalField(max_digits=6, verbose_name='权重 体重', decimal_places=4)),
                ('weight_p_bmi', models.DecimalField(max_digits=6, verbose_name='权重 BMI', decimal_places=4)),
                ('const', models.DecimalField(max_digits=6, verbose_name='常量', decimal_places=4)),
                ('sport', models.ForeignKey(to='sportsman.Sport', verbose_name='体育项目')),
            ],
            options={
                'verbose_name': '体育项目潜质参数',
                'verbose_name_plural': '体育项目潜质参数',
            },
        ),
        migrations.AlterModelOptions(
            name='factor',
            options={'verbose_name_plural': '测试项目成绩分布参数', 'verbose_name': '测试项目成绩分布参数'},
        ),
        migrations.AddField(
            model_name='factor',
            name='mean_bmi',
            field=models.DecimalField(max_digits=3, verbose_name='BMI平均值', default=0, decimal_places=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='mean_height',
            field=models.DecimalField(max_digits=4, verbose_name='身高（厘米）平均值', default=0, decimal_places=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='mean_weight',
            field=models.DecimalField(max_digits=5, verbose_name='体重（公斤）平均值', default=0, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='standard_deviation_bmi',
            field=models.DecimalField(max_digits=10, verbose_name='BMI标准偏差', default=0, decimal_places=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='standard_deviation_height',
            field=models.DecimalField(max_digits=10, verbose_name='身高（厘米）标准偏差', default=0, decimal_places=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factor',
            name='standard_deviation_weight',
            field=models.DecimalField(max_digits=10, verbose_name='体重（公斤）标准偏差', default=0, decimal_places=4),
            preserve_default=False,
        ),
    ]
