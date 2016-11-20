# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0002_auto_20160531_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='dataVersion',
            field=models.IntegerField(verbose_name='数据版本, 从1开始, 每保存一次便增加1.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='correspondWithStudentDataVersion',
            field=models.IntegerField(verbose_name='本评价对应的学生数据版本.(若小于当前关联学生数据的版本号, 则表明此评价可能不匹配.)', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='studentDataComplete',
            field=models.BooleanField(verbose_name='本评价对应的学生数据是否完整', default=True),
            preserve_default=False,
        ),
    ]
