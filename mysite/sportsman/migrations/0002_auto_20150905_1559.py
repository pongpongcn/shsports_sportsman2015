# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='gender',
            field=models.CharField(choices=[('MALE', '男'), ('FEMALE', '女')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='factor',
            name='movement_type',
            field=models.CharField(choices=[('20m', '20米跑'), ('bal', '后退平衡'), ('shh', '侧向跳'), ('rb', '躯体')], max_length=10, null=True),
        ),
    ]
