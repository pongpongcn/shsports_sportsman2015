# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sportsman', '0002_auto_20160515_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='creator',
            field=models.ForeignKey(verbose_name='创建者', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
