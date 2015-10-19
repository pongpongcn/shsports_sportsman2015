# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0007_auto_20151017_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='addition',
            field=models.CharField(blank=True, verbose_name='号（地址）', null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='addressClearance',
            field=models.NullBooleanField(default=False, verbose_name='地址Clearance'),
        ),
        migrations.AlterField(
            model_name='student',
            name='city',
            field=models.CharField(blank=True, verbose_name='城市（地址）', null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='housenumber',
            field=models.CharField(blank=True, verbose_name='弄（地址）', null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='street',
            field=models.CharField(blank=True, verbose_name='路（地址）', null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='universalFirstName',
            field=models.CharField(blank=True, verbose_name='名（英文）', null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='universalLastName',
            field=models.CharField(blank=True, verbose_name='姓（英文）', null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='zip',
            field=models.CharField(blank=True, verbose_name='邮政编码（地址）', null=True, max_length=255),
        ),
    ]
