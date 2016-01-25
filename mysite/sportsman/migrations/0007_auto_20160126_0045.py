# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0006_auto_20160126_0037'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='名称', max_length=100)),
            ],
            options={
                'verbose_name': '区县',
                'verbose_name_plural': '区县',
            },
        ),
        migrations.AddField(
            model_name='school',
            name='district',
            field=models.ForeignKey(null=True, to='sportsman.District', verbose_name='所属区县', blank=True),
        ),
    ]
