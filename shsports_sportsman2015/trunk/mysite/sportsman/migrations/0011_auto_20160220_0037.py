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
        migrations.AddField(
            model_name='studentevaluation',
            name='p_20m',
            field=models.DecimalField(max_digits=2, decimal_places=2, blank=True, verbose_name='累积概率 20米冲刺跑', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_bal',
            field=models.DecimalField(max_digits=2, decimal_places=2, blank=True, verbose_name='累积概率 平衡', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_ball',
            field=models.DecimalField(max_digits=2, decimal_places=2, blank=True, verbose_name='累积概率 投掷', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_bmi',
            field=models.DecimalField(max_digits=2, decimal_places=2, blank=True, verbose_name='累积概率 BMI', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_height',
            field=models.DecimalField(max_digits=2, decimal_places=2, blank=True, verbose_name='累积概率 身高', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_lauf',
            field=models.DecimalField(max_digits=2, decimal_places=2, blank=True, verbose_name='累积概率 六分跑', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_ls',
            field=models.DecimalField(max_digits=2, decimal_places=2, blank=True, verbose_name='累积概率 俯卧撑', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_rb',
            field=models.DecimalField(max_digits=2, decimal_places=2, blank=True, verbose_name='累积概率 直身前屈', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_shh',
            field=models.DecimalField(max_digits=2, decimal_places=2, blank=True, verbose_name='累积概率 侧向跳', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_su',
            field=models.DecimalField(max_digits=2, decimal_places=2, blank=True, verbose_name='累积概率 仰卧起坐', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_sws',
            field=models.DecimalField(max_digits=2, decimal_places=2, blank=True, verbose_name='累积概率 跳远', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='p_weight',
            field=models.DecimalField(max_digits=2, decimal_places=2, blank=True, verbose_name='累积概率 体重', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_athletics_running',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 耐力跑', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_athletics_sprinting_jumping_throwing',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 跑跳投', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_badminton',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 羽毛球', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_basketball',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 篮球', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_canoe',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 皮艇/划艇', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_discus',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 铁饼', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_gymnastics',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 体操', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_high_jump',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 跳高', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_huerdles',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 跨栏', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_javelin',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 标枪', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_long_jump',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 跳远', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_pole_vault',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 撑杆跳', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_rowing',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 赛艇', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_shot_put',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 铅球', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_soccer',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 足球', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_sprint',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 短跑', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_swimming',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 游泳', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_table_tennis',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 乒乓球', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_tennis',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 网球', null=True),
        ),
        migrations.AddField(
            model_name='studentevaluation',
            name='potential_volleyball',
            field=models.DecimalField(max_digits=3, decimal_places=3, blank=True, verbose_name='运动潜质 排球', null=True),
        ),
        migrations.AlterField(
            model_name='studentevaluation',
            name='score_sum',
            field=models.DecimalField(max_digits=19, decimal_places=2, verbose_name='总分'),
        ),
    ]
