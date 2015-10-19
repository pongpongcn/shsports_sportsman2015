# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0004_auto_20151017_1308'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='school',
            options={'verbose_name': '学校', 'verbose_name_plural': '学校'},
        ),
        migrations.AlterModelOptions(
            name='schoolclass',
            options={'verbose_name': '班级', 'verbose_name_plural': '班级'},
        ),
        migrations.RenameField(
            model_name='schoolclass',
            old_name='student',
            new_name='school',
        ),
        migrations.AddField(
            model_name='student',
            name='schoolClass',
            field=models.ForeignKey(to='sportsman.SchoolClass', default=0),
            preserve_default=False,
        ),
    ]
