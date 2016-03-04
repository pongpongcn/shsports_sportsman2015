# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0012_auto_20160302_0048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testrefdata',
            name='student',
        ),
        migrations.RemoveField(
            model_name='testrefdataitem',
            name='test_ref_data',
        ),
        migrations.RemoveField(
            model_name='testsummarydata',
            name='student',
        ),
        migrations.RemoveField(
            model_name='testsummarydata',
            name='test_ref_data',
        ),
        migrations.RemoveField(
            model_name='testsummarydataitem',
            name='test_summary_data',
        ),
        migrations.DeleteModel(
            name='TestRefData',
        ),
        migrations.DeleteModel(
            name='TestRefDataItem',
        ),
        migrations.DeleteModel(
            name='TestSummaryData',
        ),
        migrations.DeleteModel(
            name='TestSummaryDataItem',
        ),
    ]
