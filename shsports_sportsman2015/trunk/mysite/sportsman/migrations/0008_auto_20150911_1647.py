# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0007_auto_20150905_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testrefdata',
            name='student',
            field=models.ForeignKey(to='sportsman.Student', verbose_name='测试学生'),
        ),
        migrations.AlterField(
            model_name='testrefdataitem',
            name='test_ref_data',
            field=models.ForeignKey(to='sportsman.TestRefData', verbose_name='测试原始记录'),
        ),
    ]
