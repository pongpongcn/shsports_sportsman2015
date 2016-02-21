# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0011_auto_20160220_2225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentevaluation',
            name='certificate',
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='certificate_data',
            field=models.TextField(null=True, max_length=255, verbose_name='证书数据', blank=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='certificate_file',
            field=models.FileField(null=True, upload_to='certificates/%Y/%m/%d/', verbose_name='证书文件', blank=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='certificate_template',
            field=models.CharField(null=True, max_length=255, verbose_name='证书模板', blank=True),
        ),
    ]
