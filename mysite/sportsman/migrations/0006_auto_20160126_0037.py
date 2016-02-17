# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0005_auto_20160117_1228'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': '学生', 'verbose_name_plural': '学生', 'permissions': (('import_student', '可以导入学生'), ('export_student', '可以导出学生'), ('evaluate_student', '可以评价学生'))},
        ),
    ]