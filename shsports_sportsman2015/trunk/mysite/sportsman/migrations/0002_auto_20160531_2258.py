# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sportsman', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('code', models.CharField(verbose_name='代码', unique=True, max_length=50)),
                ('name', models.CharField(verbose_name='名称', max_length=50)),
                ('universalName', models.CharField(verbose_name='名称（英文）', max_length=50)),
            ],
            options={
                'verbose_name': '体育项目',
                'verbose_name_plural': '体育项目',
            },
        ),
        migrations.CreateModel(
            name='SportPotentialFactor',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
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
            options={'verbose_name': '测试项目成绩分布参数', 'verbose_name_plural': '测试项目成绩分布参数'},
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
        migrations.AddField(
            model_name='student',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='创建者', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='student',
            name='x_jichudaixie',
            field=models.CharField(verbose_name='基础代谢', blank=True, null=True, max_length=255),
        ),
        migrations.AddField(
            model_name='student',
            name='x_jirou',
            field=models.CharField(verbose_name='肌肉', blank=True, null=True, max_length=255),
        ),
        migrations.AddField(
            model_name='student',
            name='x_shuifen',
            field=models.CharField(verbose_name='水分', blank=True, null=True, max_length=255),
        ),
    ]
