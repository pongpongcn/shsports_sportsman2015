# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0006_auto_20151017_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='addition',
            field=models.CharField(null=True, max_length=255, verbose_name='号（地址）'),
        ),
        migrations.AddField(
            model_name='student',
            name='addressClearance',
            field=models.BooleanField(verbose_name='地址Clearance', default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='city',
            field=models.CharField(null=True, max_length=255, verbose_name='城市（地址）'),
        ),
        migrations.AddField(
            model_name='student',
            name='dateOfBirth',
            field=models.DateField(null=True, verbose_name='出生日期'),
        ),
        migrations.AddField(
            model_name='student',
            name='dateOfTesting',
            field=models.DateField(null=True, verbose_name='测试日期'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_20m_1',
            field=models.DecimalField(max_digits=19, decimal_places=2, null=True, verbose_name='20米冲刺跑1'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_20m_2',
            field=models.DecimalField(max_digits=19, decimal_places=2, null=True, verbose_name='20米冲刺跑2'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_bal30_1',
            field=models.IntegerField(null=True, blank=True, verbose_name='3厘米平衡木1'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_bal30_2',
            field=models.IntegerField(null=True, blank=True, verbose_name='3厘米平衡木2'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_bal45_1',
            field=models.IntegerField(null=True, blank=True, verbose_name='4.5厘米平衡木1'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_bal45_2',
            field=models.IntegerField(null=True, blank=True, verbose_name='4.5厘米平衡木2'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_bal60_1',
            field=models.IntegerField(null=True, blank=True, verbose_name='6厘米平衡木1'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_bal60_2',
            field=models.IntegerField(null=True, blank=True, verbose_name='6厘米平衡木2'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_ball_1',
            field=models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True, verbose_name='投掷1'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_ball_2',
            field=models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True, verbose_name='投掷2'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_ball_3',
            field=models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True, verbose_name='投掷3'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_lauf_rest',
            field=models.IntegerField(null=True, blank=True, verbose_name='六分跑剩余距离'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_lauf_runden',
            field=models.IntegerField(null=True, blank=True, verbose_name='六分跑圈数'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_ls',
            field=models.IntegerField(null=True, blank=True, verbose_name='俯卧撑'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_rb_1',
            field=models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True, verbose_name='直身前屈1'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_rb_2',
            field=models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True, verbose_name='直身前屈2'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_shh_1f',
            field=models.IntegerField(null=True, blank=True, verbose_name='侧向跳1 错误'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_shh_1s',
            field=models.IntegerField(null=True, blank=True, verbose_name='侧向跳1 次'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_shh_2f',
            field=models.IntegerField(null=True, blank=True, verbose_name='侧向跳2 错误'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_shh_2s',
            field=models.IntegerField(null=True, blank=True, verbose_name='侧向跳2 次'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_slauf_10',
            field=models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True, verbose_name='星形跑重复10次'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_su',
            field=models.IntegerField(null=True, blank=True, verbose_name='仰卧起坐'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_sws_1',
            field=models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True, verbose_name='跳远1'),
        ),
        migrations.AddField(
            model_name='student',
            name='e_sws_2',
            field=models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True, verbose_name='跳远2'),
        ),
        migrations.AddField(
            model_name='student',
            name='firstName',
            field=models.CharField(verbose_name='名', max_length=255, default='noName'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='height',
            field=models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True, verbose_name='身高（厘米）'),
        ),
        migrations.AddField(
            model_name='student',
            name='housenumber',
            field=models.CharField(null=True, max_length=255, verbose_name='弄（地址）'),
        ),
        migrations.AddField(
            model_name='student',
            name='lastName',
            field=models.CharField(verbose_name='姓', max_length=255, default='noLastName'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='number',
            field=models.IntegerField(null=True, verbose_name='测试号码'),
        ),
        migrations.AddField(
            model_name='student',
            name='questionary',
            field=models.IntegerField(null=True, verbose_name='问卷编号'),
        ),
        migrations.AddField(
            model_name='student',
            name='street',
            field=models.CharField(null=True, max_length=255, verbose_name='路（地址）'),
        ),
        migrations.AddField(
            model_name='student',
            name='universalFirstName',
            field=models.CharField(null=True, max_length=255, verbose_name='名（英文）'),
        ),
        migrations.AddField(
            model_name='student',
            name='universalLastName',
            field=models.CharField(null=True, max_length=255, verbose_name='姓（英文）'),
        ),
        migrations.AddField(
            model_name='student',
            name='weight',
            field=models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True, verbose_name='体重（千克）'),
        ),
        migrations.AddField(
            model_name='student',
            name='zip',
            field=models.CharField(null=True, max_length=255, verbose_name='邮政编码（地址）'),
        ),
        migrations.AlterField(
            model_name='schoolclass',
            name='school',
            field=models.ForeignKey(to='sportsman.School', verbose_name='学校'),
        ),
        migrations.AlterField(
            model_name='student',
            name='schoolClass',
            field=models.ForeignKey(to='sportsman.SchoolClass', verbose_name='班级'),
        ),
    ]
