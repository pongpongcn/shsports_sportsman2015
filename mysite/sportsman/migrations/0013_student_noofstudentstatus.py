# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0012_auto_20151020_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='noOfStudentStatus',
            field=models.CharField(verbose_name='学籍号', null=True, max_length=255, blank=True),
        ),
    ]
