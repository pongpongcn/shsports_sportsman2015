# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsman', '0010_auto_20160217_1805'),
    ]

    operations = [
        migrations.RenameField(
            model_name='standardparameter',
            old_name='original_score_20m',
            new_name='e_20m',
        ),
        migrations.RenameField(
            model_name='standardparameter',
            old_name='original_score_bal',
            new_name='e_bal',
        ),
        migrations.RenameField(
            model_name='standardparameter',
            old_name='original_score_ball',
            new_name='e_ball',
        ),
        migrations.RenameField(
            model_name='standardparameter',
            old_name='original_score_lauf',
            new_name='e_lauf',
        ),
        migrations.RenameField(
            model_name='standardparameter',
            old_name='original_score_ls',
            new_name='e_ls',
        ),
        migrations.RenameField(
            model_name='standardparameter',
            old_name='original_score_rb',
            new_name='e_rb',
        ),
        migrations.RenameField(
            model_name='standardparameter',
            old_name='original_score_shh',
            new_name='e_shh',
        ),
        migrations.RenameField(
            model_name='standardparameter',
            old_name='original_score_su',
            new_name='e_su',
        ),
        migrations.RenameField(
            model_name='standardparameter',
            old_name='original_score_sws',
            new_name='e_sws',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='age',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='bmi',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='day_age',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='month_age',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='original_score_20m',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='original_score_bal',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='original_score_ball',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='original_score_lauf',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='original_score_ls',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='original_score_rb',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='original_score_shh',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='original_score_su',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='original_score_sws',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='percentage_20m',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='percentage_bal',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='percentage_ball',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='percentage_lauf',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='percentage_ls',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='percentage_rb',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='percentage_shh',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='percentage_su',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='percentage_sws',
        ),
        migrations.RemoveField(
            model_name='studentevaluation',
            name='score_sum',
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='certificate_data',
            field=models.TextField(blank=True, verbose_name='证书数据', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='certificate_file',
            field=models.FileField(blank=True, verbose_name='证书文件', null=True, upload_to='certificates/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='is_frail',
            field=models.BooleanField(verbose_name='需要健康干预', default=False),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='is_talent',
            field=models.BooleanField(verbose_name='运动天赋优秀', default=False),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_20m',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='百分等级 20米冲刺跑', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_bal',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='百分等级 平衡', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_ball',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='百分等级 投掷', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_bmi',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='百分等级 BMI', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_height',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='百分等级 身高', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_lauf',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='百分等级 六分跑', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_ls',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='百分等级 俯卧撑', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_rb',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='百分等级 直身前屈', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_shh',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='百分等级 侧向跳', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_su',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='百分等级 仰卧起坐', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_sws',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='百分等级 跳远', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_weight',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='百分等级 体重', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_athletics_running',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 耐力跑', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_athletics_sprinting_jumping_throwing',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 跑跳投', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_badminton',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 羽毛球', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_basketball',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 篮球', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_canoe',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 皮艇/划艇', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_discus',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 铁饼', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_gymnastics',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 体操', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_high_jump',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 跳高', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_huerdles',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 跨栏', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_javelin',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 标枪', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_long_jump',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 跳远', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_pole_vault',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 撑杆跳', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_rowing',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 赛艇', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_shot_put',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 铅球', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_soccer',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 足球', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_sprint',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 短跑', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_swimming',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 游泳', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_table_tennis',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 乒乓球', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_tennis',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 网球', max_digits=7, null=True, decimal_places=6),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_volleyball',
            field=models.DecimalField(blank=True, verbose_name='运动潜质 排球', max_digits=7, null=True, decimal_places=6),
        ),
    ]
