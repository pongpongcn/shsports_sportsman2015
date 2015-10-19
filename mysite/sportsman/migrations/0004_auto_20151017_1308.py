# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0003_auto_20151017_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='姓', max_length=100)),
                ('universalName', models.CharField(verbose_name='名称（英文）', max_length=100)),
            ],
            options={
                'verbose_name': '学校',
            },
        ),
        migrations.CreateModel(
            name='SchoolClass',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='姓', max_length=100)),
                ('universalName', models.CharField(verbose_name='名称（英文）', max_length=100)),
                ('student', models.ForeignKey(to='sportsman.School')),
            ],
            options={
                'verbose_name': '班级',
            },
        ),
        migrations.AlterField(
            model_name='factor',
            name='movement_type',
            field=models.CharField(verbose_name='测试点', choices=[('20m', '20米冲刺跑'), ('bal', '平衡'), ('shh', '侧向跳'), ('rb', '直身前驱'), ('ball', '投掷'), ('ls', '俯卧撑'), ('su', '仰卧起坐'), ('sws', '跳远'), ('lauf', '六分跑'), ('slauf', '星形跑')], max_length=10),
        ),
        migrations.AlterField(
            model_name='testrefdataitem',
            name='movement_type',
            field=models.CharField(verbose_name='测试点', choices=[('20m', '20米冲刺跑'), ('bal', '平衡'), ('shh', '侧向跳'), ('rb', '直身前驱'), ('ball', '投掷'), ('ls', '俯卧撑'), ('su', '仰卧起坐'), ('sws', '跳远'), ('lauf', '六分跑'), ('slauf', '星形跑')], max_length=10),
        ),
        migrations.AlterField(
            model_name='testsummarydataitem',
            name='movement_type',
            field=models.CharField(verbose_name='测试点', choices=[('20m', '20米冲刺跑'), ('bal', '平衡'), ('shh', '侧向跳'), ('rb', '直身前驱'), ('ball', '投掷'), ('ls', '俯卧撑'), ('su', '仰卧起坐'), ('sws', '跳远'), ('lauf', '六分跑'), ('slauf', '星形跑')], max_length=10),
        ),
    ]
