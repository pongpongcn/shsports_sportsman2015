from django.contrib import admin
from django import forms
from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.db.models.fields import BLANK_CHOICE_DASH
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin, base_formats
from import_export.formats.base_formats import TextFormat
from import_export.instance_loaders import ModelInstanceLoader
import calendar, os, pinyin
from django.utils import timezone
from statistics import mean
import scipy.stats
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts
from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape, letter
from reportlab.lib.units import cm, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, BaseDocTemplate, Frame, PageBreak, PageTemplate, Table, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.tables import TableStyle
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib import colors
from PyPDF2 import PdfFileWriter, PdfFileReader
from decimal import Decimal
from django.core.validators import *
import csv
from django.utils.encoding import smart_str
from django.contrib.auth import get_permission_codename
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Factor
from .models import Student
from .models import StudentEvaluation
from .models import TestRefData
from .models import TestRefDataItem
from .models import TestSummaryData
from .models import TestSummaryDataItem
from .models import UserProfile
from .models import District
from .models import School
from .models import SchoolClass
from .models import SequenceNumber
from .models import Genders
from .models import StandardParameter

# Register your models here.
MovementTypeKeys = (
        ('20m_1', '20米冲刺跑 - 第1次跑'),
        ('20m_2', '20米冲刺跑 - 第2次跑'),
        ('bal60_1', '平衡 - 6.0厘米 第1次'),
        ('bal60_2', '平衡 - 6.0厘米 第2次'),
        ('bal45_1', '平衡 - 4.5厘米 第1次'),
        ('bal45_2', '平衡 - 4.5厘米 第2次'),
        ('bal30_1', '平衡 - 3.0厘米 第1次'),
        ('bal30_2', '平衡 - 3.0厘米 第2次'),
        ('shh_1s', '侧向跳 - 第1次跳 成功'),
        ('shh_1f', '侧向跳 - 第1次跳 失败'),
        ('shh_2s', '侧向跳 - 第2次跳 成功'),
        ('shh_2f', '侧向跳 - 第2次跳 失败'),
        ('rb_1', '直身前驱 - 第1次'),
        ('rb_2', '直身前驱 - 第2次'),
        ('ball_1', '投掷 - 第1次'),
        ('ball_2', '投掷 - 第2次'),
        ('ball_3', '投掷 - 第3次'),
        ('ls', '俯卧撑'),
        ('su', '仰卧起坐'),
        ('sws_1', '跳远 - 第1次'),
        ('sws_2', '跳远 - 第2次'),
        ('lauf_runden', '六分跑 - 圈数'),
        ('lauf_rest', '六分跑 - 剩余距离'),
    )

class StandardParameterResource(resources.ModelResource):
    class Meta:
        model = StandardParameter
        import_id_fields = ('version', 'gender','age','percentile')
        exclude = ('id',)

class StandardParameterAdmin(ImportExportModelAdmin):
    resource_class = StandardParameterResource
    list_display = ('version', 'gender', 'age', 'percentile', 'original_score_20m', 'original_score_bal', 'original_score_shh', 'original_score_rb', 'original_score_ls', 'original_score_su', 'original_score_sws', 'original_score_ball', 'original_score_lauf')
    list_filter = ('version', 'gender', 'age')
    ordering = ('version', 'gender', 'age')

class FactorResource(resources.ModelResource):
    class Meta:
        model = Factor
        import_id_fields = ('version', 'gender','month_age')
        exclude = ('id',)

class FactorAdmin(ImportExportModelAdmin):
    resource_class = FactorResource
    list_display = ('version', 'gender', 'month_age', 'mean_20m', 'standard_deviation_20m', 'mean_bal', 'standard_deviation_bal', 'mean_shh', 'standard_deviation_shh', 'mean_rb', 'standard_deviation_rb', 'mean_ls', 'standard_deviation_ls', 'mean_su', 'standard_deviation_su', 'mean_sws', 'standard_deviation_sws', 'mean_ball', 'standard_deviation_ball', 'mean_lauf', 'standard_deviation_lauf')
    list_filter = ('version', 'gender', 'month_age')
    ordering = ('version', 'gender', 'month_age')
    
class StudentImportResource(resources.ModelResource):
    def before_import(self, dataset, dry_run, **kwargs):
        schoolClasses = []
        genders = []
        universalFirstNames = []
        universalLastNames = []
        for row in dataset.dict:
            schoolClass = self.get_schoolClass(row['学校'], row['班级'])
            schoolClasses.append(schoolClass)
            gender = self.get_gender(row['性别'])
            genders.append(gender)
            universalFirstNames.append(pinyin.get(row['名'], format="strip").capitalize())
            universalLastNames.append(pinyin.get(row['姓'], format="strip").capitalize())
        dataset.append_col(schoolClasses, header='schoolClass')
        dataset.append_col(genders, header='gender')
        dataset.append_col(universalFirstNames, header='universalFirstName')
        dataset.append_col(universalLastNames, header='universalLastName')
    def get_schoolClass(self, schoolName, schoolClassName):
        schoolQuery = School.objects.filter(name=schoolName)
        if schoolQuery.exists():
            school = schoolQuery[0]
        else:
            school = School(name=schoolName, universalName='')
            school.save()
        schoolClassQuery = SchoolClass.objects.filter(school=school, name=schoolClassName)
        if schoolClassQuery.exists():
            schoolClass = schoolClassQuery[0]
        else:
            schoolClass = SchoolClass(school=school, name=schoolClassName, universalName='')
            schoolClass.save()
        return schoolClass
    def get_gender(self, genderName):
        if genderName == '男':
            return 'MALE'
        elif genderName == '女':
            return 'FEMALE'
        else:
            return None

    noOfStudentStatus = fields.Field(attribute='noOfStudentStatus', column_name='学籍号')
    firstName = fields.Field(attribute='firstName', column_name='名')
    lastName = fields.Field(attribute='lastName', column_name='姓')
    dateOfBirth = fields.Field(attribute='dateOfBirth', column_name='出生日期')
    dateOfTesting = fields.Field(attribute='dateOfTesting', column_name='测试日期')
    schoolClass = fields.Field(attribute='schoolClass', column_name='班级(内部对象)')
    gender = fields.Field(attribute='gender', column_name='性别(内部值)')
    universalFirstName = fields.Field(attribute='universalFirstName', column_name='First Name')
    universalLastName = fields.Field(attribute='universalLastName', column_name='Last Name')
    class Meta:
        model = Student
        import_id_fields = ('noOfStudentStatus',)
        fields = ()
        #Does not working until now.
        skip_unchanged = True

class StudentResource(resources.ModelResource):
    numberTalentCheck = fields.Field()
    className = fields.Field()
    universalClassName = fields.Field()
    schoolName = fields.Field()
    universalSchoolName = fields.Field()
    dateOfTalentCheck = fields.Field()
    selectedForTalentCheck = fields.Field()
    addressClearance = fields.Field()
    e_20m = fields.Field()
    e_bal = fields.Field()
    e_shh = fields.Field()
    e_rb = fields.Field()
    e_sws = fields.Field()
    e_ball = fields.Field()
    e_lauf = fields.Field()
    comment = fields.Field()
    e_15m_sw = fields.Field()
    e_15m_sw_bbs = fields.Field()
    e_15m_sw_ns = fields.Field()
    e_10m_ped_1 = fields.Field()
    e_10m_ped_2 = fields.Field()
    e_10m_ped = fields.Field()
    e_tt_15s_1 = fields.Field()
    e_tt_15s_2 = fields.Field()
    e_tt_15s = fields.Field()
    e_fb_drib_ob_1 = fields.Field()
    e_fb_drib_ob_2 = fields.Field()
    e_fb_drib_ob = fields.Field()
    e_fb_drib_mb_1 = fields.Field()
    e_fb_drib_mb_2 = fields.Field()
    e_fb_drib_mb = fields.Field()
    z_20m = fields.Field()
    z_bal = fields.Field()
    z_shh = fields.Field()
    z_rb = fields.Field()
    z_sws = fields.Field()
    z_ball = fields.Field()
    z_lauf = fields.Field()
    z_ls = fields.Field()
    z_su = fields.Field()
    z_10m_ped = fields.Field()
    z_15m_sw = fields.Field()
    z_fb_drib_mb = fields.Field()
    z_fb_drib_ob = fields.Field()
    z_tt_15s = fields.Field()
    z_slauf_10 = fields.Field()
    z_height = fields.Field()
    z_weight = fields.Field()
    z_bmi = fields.Field()
    p_20m = fields.Field()
    p_bal = fields.Field()
    p_shh = fields.Field()
    p_rb = fields.Field()
    p_ls = fields.Field()
    p_su = fields.Field()
    p_sws = fields.Field()
    p_ball = fields.Field()
    p_lauf = fields.Field()
    p_height = fields.Field()
    p_weight = fields.Field()
    p_bmi = fields.Field()
    p_10m_ped = fields.Field()
    p_15m_sw = fields.Field()
    p_fb_drib_mb = fields.Field()
    p_fb_drib_ob = fields.Field()
    p_tt_15s = fields.Field()
    p_slauf_10 = fields.Field()
    error = fields.Field()
    
    class Meta:
        model = Student
        export_order = ('id','firstName','lastName','universalFirstName','universalLastName','street','housenumber','addition','zip','city','gender','questionary','number','numberTalentCheck','weight','height','dateOfBirth','className','universalClassName','schoolName','universalSchoolName','dateOfTesting','dateOfTalentCheck','selectedForTalentCheck','addressClearance','e_20m_1','e_20m_2','e_20m','e_bal60_1','e_bal60_2','e_bal45_1','e_bal45_2','e_bal30_1','e_bal30_2','e_bal','e_shh_1s','e_shh_1f','e_shh_2s','e_shh_2f','e_shh','e_rb_1','e_rb_2','e_rb','e_ls','e_su','e_sws_1','e_sws_2','e_sws','e_ball_1','e_ball_2','e_ball_3','e_ball','e_lauf_runden','e_lauf_rest','e_lauf','comment','e_15m_sw','e_15m_sw_bbs','e_15m_sw_ns','e_10m_ped_1','e_10m_ped_2','e_10m_ped','e_slauf_10','e_tt_15s_1','e_tt_15s_2','e_tt_15s','e_fb_drib_ob_1','e_fb_drib_ob_2','e_fb_drib_ob','e_fb_drib_mb_1','e_fb_drib_mb_2','e_fb_drib_mb','z_20m','z_bal','z_shh','z_rb','z_sws','z_ball','z_lauf','z_ls','z_su','z_10m_ped','z_15m_sw','z_fb_drib_mb','z_fb_drib_ob','z_tt_15s','z_slauf_10','z_height','z_weight','z_bmi','p_20m','p_bal','p_shh','p_rb','p_ls','p_su','p_sws','p_ball','p_lauf','p_height','p_weight','p_bmi','p_10m_ped','p_15m_sw','p_fb_drib_mb','p_fb_drib_ob','p_tt_15s','p_slauf_10','error')
        fields = ('id','firstName','lastName','universalFirstName','universalLastName','street','housenumber','addition','zip','city','gender','questionary','number','weight','height','dateOfBirth','dateOfTesting','e_20m_1','e_20m_2','e_bal60_1','e_bal60_2','e_bal45_1','e_bal45_2','e_bal30_1','e_bal30_2','e_shh_1s','e_shh_1f','e_shh_2s','e_shh_2f','e_rb_1','e_rb_2','e_ls','e_su','e_sws_1','e_sws_2','e_ball_1','e_ball_2','e_ball_3','e_lauf_runden','e_lauf_rest','e_slauf_10','error')
    def dehydrate_className(self, student):
        if student.schoolClass:
            return student.schoolClass.name
        else:
            return None
    def dehydrate_universalClassName(self, student):
        if student.schoolClass:
            return student.schoolClass.universalName
        else:
            return None
    def dehydrate_schoolName(self, student):
        if student.schoolClass:
            return student.schoolClass.school.name
        else:
            return None
    def dehydrate_universalSchoolName(self, student):
        if student.schoolClass:
            return student.schoolClass.school.universalName
        else:
            return None
    def dehydrate_selectedForTalentCheck(self, student):
        return 'false'
    def dehydrate_addressClearance(self, student):
        return 'true' if student.addressClearance else 'false'

    def dehydrate_weight(self, student):
        if student.weight != None:
            return student.weight
        else:
            return Decimal('0.00')
    def dehydrate_height(self, student):
        if student.height != None:
            return round(Decimal(student.height), 2)
        else:
            return Decimal('0.00')
    def dehydrate_e_20m_1(self, student):
        if student.e_20m_1 != None:
            return student.e_20m_1
        else:
            return Decimal('0.00')
    def dehydrate_e_20m_2(self, student):
        if student.e_20m_2 != None:
            return student.e_20m_2
        else:
            return Decimal('0.00')
    def dehydrate_e_bal60_1(self, student):
        if student.e_bal60_1 != None:
            return student.e_bal60_1
        else:
            return 0
    def dehydrate_e_bal60_2(self, student):
        if student.e_bal60_2 != None:
            return student.e_bal60_2
        else:
            return 0
    def dehydrate_e_bal45_1(self, student):
        if student.e_bal45_1 != None:
            return student.e_bal45_1
        else:
            return 0
    def dehydrate_e_bal45_2(self, student):
        if student.e_bal45_2 != None:
            return student.e_bal45_2
        else:
            return 0
    def dehydrate_e_bal30_1(self, student):
        if student.e_bal30_1 != None:
            return student.e_bal30_1
        else:
            return 0
    def dehydrate_e_bal30_2(self, student):
        if student.e_bal30_2 != None:
            return student.e_bal30_2
        else:
            return 0
    def dehydrate_e_shh_1s(self, student):
        if student.e_shh_1s != None:
            return student.e_shh_1s
        else:
            return 0
    def dehydrate_e_shh_1f(self, student):
        if student.e_shh_1f != None:
            return student.e_shh_1f
        else:
            return 0
    def dehydrate_e_shh_2s(self, student):
        if student.e_shh_2s != None:
            return student.e_shh_2s
        else:
            return 0
    def dehydrate_e_shh_2f(self, student):
        if student.e_shh_2f != None:
            return student.e_shh_2f
        else:
            return 0
    def dehydrate_e_rb_1(self, student):
        if student.e_rb_1 != None:
            return student.e_rb_1
        else:
            return Decimal('0.00')
    def dehydrate_e_rb_2(self, student):
        if student.e_rb_2 != None:
            return student.e_rb_2
        else:
            return Decimal('0.00')
    def dehydrate_e_ls(self, student):
        if student.e_ls != None:
            return student.e_ls
        else:
            return 0
    def dehydrate_e_su(self, student):
        if student.e_su != None:
            return student.e_su
        else:
            return 0
    def dehydrate_e_sws_1(self, student):
        if student.e_sws_1 != None:
            return student.e_sws_1
        else:
            return Decimal('0.00')
    def dehydrate_e_sws_2(self, student):
        if student.e_sws_2 != None:
            return student.e_sws_2
        else:
            return Decimal('0.00')
    def dehydrate_e_ball_1(self, student):
        if student.e_ball_1 != None:
            return student.e_ball_1
        else:
            return Decimal('0.00')
    def dehydrate_e_ball_2(self, student):
        if student.e_ball_2 != None:
            return student.e_ball_2
        else:
            return Decimal('0.00')
    def dehydrate_e_ball_3(self, student):
        if student.e_ball_3 != None:
            return student.e_ball_3
        else:
            return Decimal('0.00')
    def dehydrate_e_lauf_runden(self, student):
        if student.e_lauf_runden != None:
            return student.e_lauf_runden
        else:
            return 0
    def dehydrate_e_lauf_rest(self, student):
        if student.e_lauf_rest != None:
            return student.e_lauf_rest
        else:
            return 0
    
    def dehydrate_e_20m(self, student):
        values = (student.e_20m_1, student.e_20m_2)
        if all(value != None for value in values):
            return min(values)
        else:
            return Decimal('0.00')
    def dehydrate_e_bal(self, student):
        values = (student.e_bal60_1, student.e_bal60_2, student.e_bal45_1, student.e_bal45_2, student.e_bal30_1, student.e_bal30_2)
        if all(value != None for value in values):
            return sum(values)
        else:
            return 0
    def dehydrate_e_shh(self, student):
        values = (student.e_shh_1s, student.e_shh_1f, student.e_shh_2s, student.e_shh_2f)
        if all(value != None for value in values):
            return round(Decimal((student.e_shh_1s - student.e_shh_1f + student.e_shh_2s - student.e_shh_2f) / 2), 2)
        else:
            return Decimal('0.00')
    def dehydrate_e_rb(self, student):
        values = (student.e_rb_1, student.e_rb_2)
        if all(value != None for value in values):
            return max(values)
        else:
            return Decimal('0.00')
    def dehydrate_e_sws(self, student):
        values = (student.e_sws_1, student.e_sws_2)
        if all(value != None for value in values):
            return max(values)
        else:
            return Decimal('0.00')
    def dehydrate_e_ball(self, student):
        values = (student.e_ball_1, student.e_ball_2, student.e_ball_3)
        if all(value != None for value in values):
            return max(values)
        else:
            return Decimal('0.00')
    def dehydrate_e_lauf(self, student):
        values = (student.e_lauf_runden, student.e_lauf_rest)
        if all(value != None for value in values):
            return student.e_lauf_runden * 54 + student.e_lauf_rest
        else:
            return 0
    def dehydrate_error(self, student):
        return check_student_error(student)

def check_student_error(student):
    if not (student.weight != None and student.weight >= 10 and student.weight <= 100):
        return '体重'
    if not (student.height != None and student.height >= 80 and student.height <= 210):
        return '身高'
    e_20m_values = (student.e_20m_1, student.e_20m_2)
    if not all(value != None and value >=3.00 and value <= 9.00 for value in e_20m_values):
        return '20米跑'
    e_bal_values = (student.e_bal60_1, student.e_bal60_2, student.e_bal45_1, student.e_bal45_2, student.e_bal30_1, student.e_bal30_2)
    if not all(value != None and value >=0 and value <= 8 for value in e_bal_values):
        return '后退平衡'
    e_shh_values = (student.e_shh_1s, student.e_shh_1f, student.e_shh_2s, student.e_shh_2f)        
    if not (all(value != None for value in e_shh_values) and (student.e_shh_1s >= 8 and student.e_shh_1s <= 80 and student.e_shh_2s >= 8 and student.e_shh_2s <= 80 and student.e_shh_1f >=0 and student.e_shh_1f <= student.e_shh_1s and student.e_shh_2f >=0 and student.e_shh_2f <= student.e_shh_2s)):
        return '侧向跳'
    e_rb_values = (student.e_rb_1, student.e_rb_2)
    if not all(value != None and value >= -35 and value <= 35 for value in e_rb_values):
        return '立位体前屈'
    if not (student.e_ls != None and student.e_ls >= 0 and student.e_ls <=60):
        return '俯卧撑'
    if not (student.e_su != None and student.e_su >= 0 and student.e_su <=60):
        return '仰卧起坐'
    e_sws_values = (student.e_sws_1, student.e_sws_2)
    if not all(value != None and value >=20 and value <= 300 for value in e_sws_values):
        return '立定跳远'
    if not (student.e_lauf_runden != None and student.e_lauf_runden >= 0 and student.e_lauf_runden <= 30 and student.e_lauf_rest != None and student.e_lauf_rest >= 0 and student.e_lauf_rest <= 53):
        return '6分钟跑'
    e_ball_values = (student.e_ball_1, student.e_ball_2, student.e_ball_3)
    if not all(value != None and value >=0 and value <= 30 for value in e_ball_values):
        return '投掷球'
    return None

class StudentImportExportFormatCSV(TextFormat):
    TABLIB_MODULE = 'sportsman.formats.student_tablib_format_csv'
    CONTENT_TYPE = 'text/csv'

class StudentDataCompletedListFilter(admin.SimpleListFilter):
    title = ('数据完整情况')
    parameter_name = 'dataCompleted'
    def lookups(self, request, model_admin):
        return (
            ('True', '完整'),
            ('False', '不完整'),
        )
    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(height__isnull=False,
                                   weight__isnull=False,
                                   e_20m_1__isnull=False,
                                   e_20m_2__isnull=False,
                                   e_bal60_1__isnull=False,
                                   e_bal60_2__isnull=False,
                                   e_bal45_1__isnull=False,
                                   e_bal45_2__isnull=False,
                                   e_bal30_1__isnull=False,
                                   e_bal30_2__isnull=False,
                                   e_shh_1s__isnull=False,
                                   e_shh_1f__isnull=False,
                                   e_shh_2s__isnull=False,
                                   e_shh_2f__isnull=False,
                                   e_rb_1__isnull=False,
                                   e_rb_2__isnull=False,
                                   e_ls__isnull=False,
                                   e_su__isnull=False,
                                   e_sws_1__isnull=False,
                                   e_sws_2__isnull=False,
                                   e_lauf_runden__isnull=False,
                                   e_lauf_rest__isnull=False,
                                   e_ball_1__isnull=False,
                                   e_ball_2__isnull=False,
                                   e_ball_3__isnull=False)
        if self.value() == 'False':
            return queryset.filter(Q(height__isnull=True)|
                                   Q(weight__isnull=True)|
                                   Q(e_20m_1__isnull=True)|
                                   Q(e_20m_2__isnull=True)|
                                   Q(e_bal60_1__isnull=True)|
                                   Q(e_bal60_2__isnull=True)|
                                   Q(e_bal45_1__isnull=True)|
                                   Q(e_bal45_2__isnull=True)|
                                   Q(e_bal30_1__isnull=True)|
                                   Q(e_bal30_2__isnull=True)|
                                   Q(e_shh_1s__isnull=True)|
                                   Q(e_shh_1f__isnull=True)|
                                   Q(e_shh_2s__isnull=True)|
                                   Q(e_shh_2f__isnull=True)|
                                   Q(e_rb_1__isnull=True)|
                                   Q(e_rb_2__isnull=True)|
                                   Q(e_ls__isnull=True)|
                                   Q(e_su__isnull=True)|
                                   Q(e_sws_1__isnull=True)|
                                   Q(e_sws_2__isnull=True)|
                                   Q(e_lauf_runden__isnull=True)|
                                   Q(e_lauf_rest__isnull=True)|
                                   Q(e_ball_1__isnull=True)|
                                   Q(e_ball_2__isnull=True)|
                                   Q(e_ball_3__isnull=True))

class StudentForm(forms.ModelForm):
    height = forms.IntegerField(label='身高（厘米）', validators=[MinValueValidator(80),MaxValueValidator(210)])
    weight = forms.DecimalField(label='体重（公斤）', validators=[MinValueValidator(10),MaxValueValidator(100)])
    e_20m_1 = forms.DecimalField(label='第一次跑（秒）', validators=[MinValueValidator(3.00),MaxValueValidator(9.00)])
    e_20m_2 = forms.DecimalField(label='第二次跑（秒）', validators=[MinValueValidator(3.00),MaxValueValidator(9.00)])
    e_bal60_1 = forms.IntegerField(label='6.0厘米 第一次', validators=[MinValueValidator(0),MaxValueValidator(8)])
    e_bal60_2 = forms.IntegerField(label='6.0厘米 第二次', validators=[MinValueValidator(0),MaxValueValidator(8)])
    e_bal45_1 = forms.IntegerField(label='4.5厘米 第一次', validators=[MinValueValidator(0),MaxValueValidator(8)])
    e_bal45_2 = forms.IntegerField(label='4.5厘米 第二次', validators=[MinValueValidator(0),MaxValueValidator(8)])
    e_bal30_1 = forms.IntegerField(label='3.0厘米 第一次', validators=[MinValueValidator(0),MaxValueValidator(8)])
    e_bal30_2 = forms.IntegerField(label='3.0厘米 第二次', validators=[MinValueValidator(0),MaxValueValidator(8)])
    e_shh_1s = forms.IntegerField(label='第一次跳（总次数）', validators=[MinValueValidator(8),MaxValueValidator(80)])
    e_shh_1f = forms.IntegerField(label='第一次跳（错误次数）', validators=[MinValueValidator(0)])
    e_shh_2s = forms.IntegerField(label='第二次跳（总次数）', validators=[MinValueValidator(8),MaxValueValidator(80)])
    e_shh_2f = forms.IntegerField(label='第二次跳（错误次数）', validators=[MinValueValidator(0)])
    e_rb_1 = forms.DecimalField(label='第一次（厘米）', validators=[MinValueValidator(-35),MaxValueValidator(35)])
    e_rb_2 = forms.DecimalField(label='第二次（厘米）', validators=[MinValueValidator(-35),MaxValueValidator(35)])
    e_ls = forms.IntegerField(label='次数（40秒内）', validators=[MinValueValidator(0),MaxValueValidator(60)])
    e_su = forms.IntegerField(label='次数（40秒内）', validators=[MinValueValidator(0),MaxValueValidator(60)])
    e_sws_1 = forms.DecimalField(label='第一次（厘米）', validators=[MinValueValidator(20),MaxValueValidator(300)])
    e_sws_2 = forms.DecimalField(label='第二次（厘米）', validators=[MinValueValidator(20),MaxValueValidator(300)])
    e_lauf_runden = forms.IntegerField(label='圈数', validators=[MinValueValidator(0),MaxValueValidator(30)])
    e_lauf_rest = forms.IntegerField(label='最后未完成的一圈所跑距离（米）', validators=[MinValueValidator(0),MaxValueValidator(53)])
    e_ball_1 = forms.DecimalField(label='第一次', validators=[MinValueValidator(0),MaxValueValidator(30)])
    e_ball_2 = forms.DecimalField(label='第二次', validators=[MinValueValidator(0),MaxValueValidator(30)])
    e_ball_3 = forms.DecimalField(label='第三次', validators=[MinValueValidator(0),MaxValueValidator(30)])

    def clean(self):
        cleaned_data = super(StudentForm, self).clean()
        e_shh_1s = cleaned_data.get("e_shh_1s")
        e_shh_1f = cleaned_data.get("e_shh_1f")
        e_shh_2s = cleaned_data.get("e_shh_2s")
        e_shh_2f = cleaned_data.get("e_shh_2f")

        if e_shh_1s and e_shh_1f:
            if e_shh_1s < e_shh_1f:
                msg = "错误次数不能超过总次数"
                self.add_error('e_shh_1f', msg)

        if e_shh_2s and e_shh_2f:
            if e_shh_2s < e_shh_2f:
                msg = "错误次数不能超过总次数"
                self.add_error('e_shh_2f', msg)


class StudentAdmin(ImportExportModelAdmin):
    form = StudentForm
    resource_class = StudentResource
    formats = (
        StudentImportExportFormatCSV,
        base_formats.XLS,
        base_formats.HTML,
    )

    def get_actions(self, request):
        actions = super(StudentAdmin, self).get_actions(request)
        if not self.has_evaluate_permission(request):
            if 'evaluate_selected' in actions:
                del actions['evaluate_selected']
        return actions
    actions = ['evaluate_selected']
    
    def get_import_resource_class(self):
        return StudentImportResource

    date_hierarchy = 'dateOfTesting'
    fieldsets = (
        (None, {
            'fields': ('noOfStudentStatus', ('school', 'schoolClass'), ('firstName', 'lastName'), ('universalFirstName', 'universalLastName'), 'gender', 'dateOfBirth', ('dateOfTesting', 'number'))
            }),
        ('地址', {
            'classes': ('wide',),
            'fields': (('street', 'housenumber'), 'addition', ('zip', 'city'))
            }),
        ('测试成绩', {
            'classes': ('wide',),
            'fields': ()
            }),
        (None, {
            'classes': ('wide',),
            'fields': (('height', 'weight'),)
            }),
        ('测试1: 20米跑', {
            'classes': ('wide',),
            'fields': (('e_20m_1', 'e_20m_2'),)
            }),
        ('测试2: 后退平衡', {
            'classes': ('wide',),
            'fields': (('e_bal60_1', 'e_bal60_2'), ('e_bal45_1', 'e_bal45_2'), ('e_bal30_1', 'e_bal30_2'))
            }),
        ('测试3: 侧向跳', {
            'classes': ('wide',),
            'fields': (('e_shh_1s', 'e_shh_1f'), ('e_shh_2s', 'e_shh_2f'),)
            }),
        ('测试4: 立位体前屈', {
            'classes': ('wide',),
            'fields': (('e_rb_1', 'e_rb_2'),)
            }),
        ('测试5: 俯卧撑', {
            'classes': ('wide',),
            'fields': ('e_ls',)
            }),
        ('测试6: 仰卧起坐', {
            'classes': ('wide',),
            'fields': ('e_su',)
            }),
        ('测试7: 立定跳远', {
            'classes': ('wide',),
            'fields': (('e_sws_1', 'e_sws_2'),)
            }),
        ('测试8: 6分钟跑', {
            'classes': ('wide',),
            'fields': (('e_lauf_runden', 'e_lauf_rest'),)
            }),
        ('测试9: 投掷球', {
            'classes': ('wide',),
            'fields': (('e_ball_1', 'e_ball_2', 'e_ball_3'),)
            }),
        ('其它', {
            'classes': ('collapse',),
            'fields': ('questionary', 'addressClearance', 'external_id','e_slauf_10',)
            })
    )
    
    def school(self, instance):
        return instance.schoolClass.school
    school.short_description = '学校'
    school.admin_order_field = 'schoolClass__school'
	
    def district(self, instance):
        return instance.schoolClass.school.district
    district.short_description = '区县'
    district.admin_order_field = 'schoolClass__school__district'

    def get_queryset(self, request):
        queryset=super(StudentAdmin, self).get_queryset(request)
        currentUser = request.user
        if currentUser.groups.filter(name='district_users').count() > 0:
            district = None
            try:
                userprofile = currentUser.userprofile
                if userprofile.district != None:
                    district = currentUser.userprofile.district
            except:
                pass
            if district != None:
                queryset=queryset.filter(schoolClass__school__district=district)
            else:
                queryset=Student.objects.none()
        return queryset

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_evaluate_permission'] = self.has_evaluate_permission(request)
        return super(StudentAdmin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_evaluate_permission'] = self.has_evaluate_permission(request)
        extra_context['has_import_permission'] = self.has_import_permission(request)
        extra_context['has_export_permission'] = self.has_export_permission(request)
        return super(StudentAdmin, self).changelist_view(request, extra_context=extra_context)

    def has_evaluate_permission(self, request):
        """
        Returns True if the given request has permission to evaluate an object.
        Can be overridden by the user in subclasses.
        """
        opts = self.opts
        codename = get_permission_codename('evaluate', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))
    
    def has_import_permission(self, request):
        """
        Returns True if the given request has permission to import an object.
        Can be overridden by the user in subclasses.
        """
        opts = self.opts
        codename = get_permission_codename('import', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def has_export_permission(self, request):
        """
        Returns True if the given request has permission to export an object.
        Can be overridden by the user in subclasses.
        """
        opts = self.opts
        codename = get_permission_codename('export', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def dataCompleted(self, instance):
        values = (instance.height,
                  instance.weight,
                  instance.e_20m_1,
                  instance.e_20m_2,
                  instance.e_bal60_1,
                  instance.e_bal60_2,
                  instance.e_bal45_1,
                  instance.e_bal45_2,
                  instance.e_bal30_1,
                  instance.e_bal30_2,
                  instance.e_shh_1s,
                  instance.e_shh_1f,
                  instance.e_shh_2s,
                  instance.e_shh_2f,
                  instance.e_rb_1,
                  instance.e_rb_2,
                  instance.e_ls,
                  instance.e_su,
                  instance.e_sws_1,
                  instance.e_sws_2,
                  instance.e_lauf_runden,
                  instance.e_lauf_rest,
                  instance.e_ball_1,
                  instance.e_ball_2,
                  instance.e_ball_3)
        if all(value != None for value in values):
            return True
        else:
            return False
    dataCompleted.short_description = '数据完整'
    dataCompleted.boolean = True
    
    list_display = ('noOfStudentStatus', 'lastName', 'firstName', 'gender', 'dateOfBirth', 'district', 'school', 'schoolClass', 'dateOfTesting', 'number', 'dataCompleted')
    list_display_links = ('noOfStudentStatus', 'lastName', 'firstName')
    list_filter = ('dateOfTesting','schoolClass__school__district','schoolClass__school', StudentDataCompletedListFilter)
    ordering = ('dateOfTesting', 'number')
    readonly_fields = ('external_id', 'school', 'number')
    search_fields = ('lastName', 'firstName', '=number', '=noOfStudentStatus')
    radio_fields = {"gender": admin.HORIZONTAL}
    list_select_related = True#性能优化

    def get_urls(self):
        urls = super(StudentAdmin, self).get_urls()
        my_urls = [
            url(r'^(.+)/gen_data_sheet_printable/$', self.admin_site.admin_view(self.gen_data_sheet_printable)),
            url(r'^gen_data_sheet_printable/$', self.admin_site.admin_view(self.gen_data_sheet_printables)),
            url(r'^(.+)/gen_certificate_printable/$', self.admin_site.admin_view(self.gen_certificate_printable)),
            url(r'^gen_certificate_printable/$', self.admin_site.admin_view(self.gen_certificate_printables)),
            url(r'^gen_certificate_list/$', self.admin_site.admin_view(self.gen_certificate_list)),
        ]
        #New urls must appear before the exists ones.
        
        return my_urls + urls 

    def get_student_queryset(self, request):
        """
        Returns export queryset.

        Default implementation respects applied search and filters.
        """
        # copied from django/contrib/admin/options.py
        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)

        ChangeList = self.get_changelist(request)
        cl = ChangeList(request, self.model, list_display,
                        list_display_links, self.list_filter,
                        self.date_hierarchy, self.search_fields,
                        self.list_select_related, self.list_per_page,
                        self.list_max_show_all, self.list_editable,
                        self)

        # query_set has been renamed to queryset in Django 1.8
        try:
            return cl.queryset
        except AttributeError:
            return cl.query_set

    def gen_data_sheet_printables(self, request, *args, **kwargs):
        students = self.get_student_queryset(request)
        
        return self.gen_data_sheet_printable_response(students)
    
    def gen_data_sheet_printable(self, request, object_id):
        student = Student.objects.get(pk=object_id)
        
        return self.gen_data_sheet_printable_response((student,))

    def gen_certificate_printables(self, request, *args, **kwargs):
        students = self.get_student_queryset(request)
        
        return self.gen_certificate_printable_response(students)
    
    def gen_certificate_printable(self, request, object_id):
        student = Student.objects.get(pk=object_id)
        
        return self.gen_certificate_printable_response((student,))

    def gen_data_sheet_printable_response(self, students):
        pdfmetrics.registerFont(ttfonts.TTFont("simsun", "simsun.ttc"))
        pagesize = landscape(A4)
        fontName = 'simsun'

        output = PdfFileWriter()

        dictGenders = dict(Genders)

        templateImagePath = os.path.join(os.path.dirname(__file__), 'storage/DataSheetTemplate.jpg')
        templateImage = Image(templateImagePath, width=29.7*cm, height=21*cm)
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=pagesize)
        for student in students:
            templateImage.drawOn(p, 0, 0)
            p.setFont("simsun", 12)
            p.drawString(4.4*cm, pagesize[1]-2.93*cm, '%s, %s' % (student.lastName, student.firstName))
            p.drawString(11.9*cm, pagesize[1]-2.93*cm, str(student.number))
            if student.gender:
                p.drawString(3.9*cm, pagesize[1]-3.63*cm, dictGenders[student.gender])
            p.drawString(11.9*cm, pagesize[1]-3.63*cm, str(student.dateOfBirth))
            p.drawString(3.9*cm, pagesize[1]-4.35*cm, student.schoolClass.school.name)
            p.drawString(11.1*cm, pagesize[1]-4.35*cm, str(student.schoolClass))
            p.drawString(4.8*cm, pagesize[1]-5.02*cm, str(student.dateOfTesting))
            p.showPage()
            
        p.save()
        
        if len(students) == 1:
            student = students[0]
            if student.dateOfTesting and student.number:
                filename = 'Data Sheet %s %s.pdf' % (student.dateOfTesting, student.number)
            else:
                filename = 'Data Sheet.pdf'
        else:
            filename = 'Data Sheet.pdf'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + filename +'"'

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

        return response

    def gen_certificate_printable_response(self, students):
        pdfmetrics.registerFont(ttfonts.TTFont("simsun", "simsun.ttc"))
        pagesize = A4
        fontName = 'simsun'

        output = PdfFileWriter()

        dictGenders = dict(Genders)

        templateImagePath = os.path.join(os.path.dirname(__file__), 'storage/CertificateTemplate.jpg')
        templateImage = Image(templateImagePath, width=21*cm, height=29.7*cm)

        lineHeight = 0.582*cm
        stripHeight = 0.4*cm
        stripWidth = 10.47*cm
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=pagesize)
        for student in students:
            if check_student_error(student) != None:
                continue
            
            try:
                scoreItems = self.getscoreItems(student)
            except:
                continue
            
            templateImage.drawOn(p, 0, 0)
            p.setFont("simsun", 9)
            p.drawString(6*cm, pagesize[1]-7.5*cm, student.lastName)
            p.drawString(6*cm, pagesize[1]-8.05*cm, student.firstName)
            p.drawString(14*cm, pagesize[1]-7.5*cm, student.schoolClass.school.name)
            p.drawString(14*cm, pagesize[1]-8.05*cm, str(student.schoolClass))

            scoreItem_offset_x = 8.225*cm
            scoreItem_offset_y = pagesize[1]-11.1*cm

            for scoreItem in scoreItems:
                p.saveState()
                p.setFillColor(colors.HexColor('#7fd8ff'))
                p.rect(scoreItem_offset_x,scoreItem_offset_y-stripHeight,Decimal(stripWidth)*Decimal(scoreItem.percentage),stripHeight, fill=1, stroke=0)
                p.restoreState()

                formatString = '%d%%(%0.'+str(scoreItem.precision)+'f %s)'
                p.drawString(scoreItem_offset_x, scoreItem_offset_y-stripHeight+0.1*cm, formatString % (scoreItem.percentage*Decimal(100), scoreItem.original_score, scoreItem.unit))
                
                scoreItem_offset_y -= lineHeight
            
            p.showPage()
            
        p.save()
        
        if len(students) == 1:
            student = students[0]
            if student.dateOfTesting and student.number:
                filename = 'Certificate_%s_%s.pdf' % (student.dateOfTesting, student.number)
            else:
                filename = 'Certificate.pdf'
        else:
            filename = 'Certificates.pdf'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + filename +'"'

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

        return response

    def getscoreItems(self, student):
        # 评分方式，'standardParameter'或'factor'
        score_method = 'standardParameter'
        
        if student.dateOfBirth == None:
            raise Exception('数据异常: 出生日期')

        if student.dateOfTesting == None:
            raise Exception('数据异常: 测试日期')

        if student.gender == None:
            raise Exception('数据异常: 性别')

        if score_method == 'standardParameter':
            return self.getscoreItems_standardParameter(student)
        elif score_method == 'factor':
            return self.getscoreItems_factor(student)

    def getscoreItems_standardParameter(self, student):
        version = 'for_china_by_german_at_201510'

        age = calculate_age(student.dateOfBirth, student.dateOfTesting)
            
        standardParameters = StandardParameter.objects.filter(version=version, gender=student.gender, age=age)

        if not standardParameters.exists():
            raise Exception('数据异常: 没有适用的评分标准')

        scoreItems = []

        original_score_bal = sum((student.e_bal60_1, student.e_bal60_2, student.e_bal45_1, student.e_bal45_2, student.e_bal30_1, student.e_bal30_2))
        try:
            standardParameter_bal = standardParameters.filter(original_score_bal__lte=original_score_bal).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_bal.percentile*Decimal(0.01), original_score_bal, '步'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_bal, '步'))

        original_score_shh = round(Decimal((student.e_shh_1s - student.e_shh_1f + student.e_shh_2s - student.e_shh_2f) / 2), 2)
        try:
            standardParameter_shh = standardParameters.filter(original_score_shh__lte=original_score_shh).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_shh.percentile*Decimal(0.01), original_score_shh, '次'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_shh, '次'))

        original_score_sws = max((student.e_sws_1, student.e_sws_2))
        try:
            standardParameter_sws = standardParameters.filter(original_score_sws__lte=original_score_sws).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_sws.percentile*Decimal(0.01), original_score_sws, '厘米'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_sws, '厘米'))

        original_score_20m = min((student.e_20m_1, student.e_20m_2))
        try:
            standardParameter_20m = standardParameters.filter(original_score_20m__gte=original_score_20m).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_20m.percentile*Decimal(0.01), original_score_20m, '秒', 2))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_20m, '秒', 2))

        original_score_su = student.e_su
        try:
            standardParameter_su = standardParameters.filter(original_score_su__lte=original_score_su).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_su.percentile*Decimal(0.01), original_score_su, '重复次数'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_su, '重复次数'))

        original_score_ls = student.e_ls
        try:
            standardParameter_ls = standardParameters.filter(original_score_ls__lte=original_score_ls).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_ls.percentile*Decimal(0.01), original_score_ls, '重复次数'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_ls, '重复次数'))

        original_score_rb = max((student.e_rb_1, student.e_rb_2))
        try:
            standardParameter_rb = standardParameters.filter(original_score_rb__lte=original_score_rb).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_rb.percentile*Decimal(0.01), original_score_rb, '厘米'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_rb, '厘米'))

        original_score_lauf = student.e_lauf_runden * 54 + student.e_lauf_rest
        try:
            standardParameter_lauf = standardParameters.filter(original_score_lauf__lte=original_score_lauf).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_lauf.percentile*Decimal(0.01), original_score_lauf, '米'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_lauf, '米'))

        original_score_ball = max((student.e_ball_1, student.e_ball_2, student.e_ball_3))
        try:
            standardParameter_ball = standardParameters.filter(original_score_ball__lte=original_score_ball).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_ball.percentile*Decimal(0.01), original_score_ball, '米'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_ball, '米'))

        return scoreItems

    def getscoreItems_factor(self, student):
        version = 'for_china_by_chinese_at_201509'

        month_age = calculate_monthdelta(student.dateOfBirth, student.dateOfTesting)

        factors = Factor.objects.filter(version=version, gender=student.gender, month_age=month_age)

        if not factors.exists():
            raise Exception('数据异常: 没有适用的评分标准')

        factor = factors[0]

        scoreItems = []

        original_score_bal = sum((student.e_bal60_1, student.e_bal60_2, student.e_bal45_1, student.e_bal45_2, student.e_bal30_1, student.e_bal30_2))
        try:
            mean = float(factor.mean_bal)
            standard_deviation = float(factor.standard_deviation_bal)
            original_score = float(original_score_bal)
            percentile = round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, original_score_bal, '步'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_bal, '步'))

        original_score_shh = round(Decimal((student.e_shh_1s - student.e_shh_1f + student.e_shh_2s - student.e_shh_2f) / 2), 2)
        try:
            mean = float(factor.mean_shh)
            standard_deviation = float(factor.standard_deviation_shh)
            original_score = float(original_score_shh)
            percentile = round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, original_score_shh, '次'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_shh, '次'))

        original_score_sws = max((student.e_sws_1, student.e_sws_2))
        try:
            mean = float(factor.mean_sws)
            standard_deviation = float(factor.standard_deviation_sws)
            original_score = float(original_score_sws)
            percentile = round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, original_score_sws, '厘米'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_sws, '厘米'))

        original_score_20m = min((student.e_20m_1, student.e_20m_2))
        try:
            mean = float(factor.mean_20m)
            standard_deviation = float(factor.standard_deviation_20m)
            original_score = float(original_score_20m)
            percentile = 1- round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, original_score_20m, '秒', 2))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_20m, '秒', 2))

        original_score_su = student.e_su
        try:
            mean = float(factor.mean_su)
            standard_deviation = float(factor.standard_deviation_su)
            original_score = float(original_score_su)
            percentile = round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, original_score_su, '重复次数'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_su, '重复次数'))

        original_score_ls = student.e_ls
        try:
            mean = float(factor.mean_ls)
            standard_deviation = float(factor.standard_deviation_ls)
            original_score = float(original_score_ls)
            percentile = round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, original_score_ls, '重复次数'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_ls, '重复次数'))

        original_score_rb = max((student.e_rb_1, student.e_rb_2))
        try:
            mean = float(factor.mean_rb)
            standard_deviation = float(factor.standard_deviation_rb)
            original_score = float(original_score_rb)
            percentile = round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, original_score_rb, '厘米'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_rb, '厘米'))

        original_score_lauf = student.e_lauf_runden * 54 + student.e_lauf_rest
        try:
            mean = float(factor.mean_lauf)
            standard_deviation = float(factor.standard_deviation_lauf)
            original_score = float(original_score_lauf)
            percentile = round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, original_score_lauf, '米'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_lauf, '米'))

        original_score_ball = max((student.e_ball_1, student.e_ball_2, student.e_ball_3))
        try:
            mean = float(factor.mean_ball)
            standard_deviation = float(factor.standard_deviation_ball)
            original_score = float(original_score_ball)
            percentile = round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, original_score_ball, '米'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), original_score_ball, '米'))

        return scoreItems

    def evaluate_selected(modeladmin, request, queryset):
        modeladmin.gen_student_evaluation_data(queryset)
        
    evaluate_selected.short_description = "评价所选的 学生"

    def gen_student_evaluation_data(self, students):
        for student in students:
            try:
                studentEvaluation = student.studentevaluation
            except:
                studentEvaluation = None

            if studentEvaluation != None:
                continue

            if check_student_error(student) != None:
                continue

            try:
                age = calculate_age(student.dateOfBirth, student.dateOfTesting)
                month_age = calculate_monthdelta(student.dateOfBirth, student.dateOfTesting)
                day_age = calculate_daydelta(student.dateOfBirth, student.dateOfTesting)
                
                BMI = round(student.weight / (student.height * Decimal(0.01)) ** 2, 1)

                scoreItems = self.getscoreItems(student)
                stand_score_sum = 0
                for scoreItem in scoreItems:
                    stand_score_sum += scoreItem.percentage * 100
                
                studentEvaluation = StudentEvaluation()
                studentEvaluation.student = student
                studentEvaluation.age = age
                studentEvaluation.month_age = month_age
                studentEvaluation.day_age = day_age
                studentEvaluation.bmi = BMI

                studentEvaluation.original_score_bal = scoreItems[0].original_score
                studentEvaluation.percentage_bal = scoreItems[0].percentage
                studentEvaluation.original_score_shh = scoreItems[1].original_score
                studentEvaluation.percentage_shh = scoreItems[1].percentage
                studentEvaluation.original_score_sws = scoreItems[2].original_score
                studentEvaluation.percentage_sws = scoreItems[2].percentage
                studentEvaluation.original_score_20m = scoreItems[3].original_score
                studentEvaluation.percentage_20m = scoreItems[3].percentage
                studentEvaluation.original_score_su = scoreItems[4].original_score
                studentEvaluation.percentage_su = scoreItems[4].percentage
                studentEvaluation.original_score_ls = scoreItems[5].original_score
                studentEvaluation.percentage_ls = scoreItems[5].percentage
                studentEvaluation.original_score_rb = scoreItems[6].original_score
                studentEvaluation.percentage_rb = scoreItems[6].percentage
                studentEvaluation.original_score_lauf = scoreItems[7].original_score
                studentEvaluation.percentage_lauf = scoreItems[7].percentage
                studentEvaluation.original_score_ball = scoreItems[8].original_score
                studentEvaluation.percentage_ball = scoreItems[8].percentage
                studentEvaluation.score_sum = stand_score_sum
                
                studentEvaluation.save()
            except Exception as e:
                print(str(e))

    def gen_certificate_list(self, request, *args, **kwargs):
        students = self.get_student_queryset(request)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=CertificatesData.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        writer.writerow([
            smart_str(u"姓"),
            smart_str(u"名"),
            smart_str(u"学校"),
            smart_str(u"班级"),
            smart_str(u"性别"),
            smart_str(u"出生日期"),
            smart_str(u"测试日期"),
            smart_str(u"年龄"),
            smart_str(u"月龄"),
            smart_str(u"备注"),
            smart_str(u"身高"),
            smart_str(u"体重"),
            smart_str(u"BMI"),
            smart_str(u"平衡"),
            smart_str(u"平衡评价"),
            smart_str(u"侧向跳"),
            smart_str(u"侧向跳评价"),
            smart_str(u"跳远"),
            smart_str(u"跳远评价"),
            smart_str(u"20米冲刺跑"),
            smart_str(u"20米冲刺跑评价"),
            smart_str(u"仰卧起坐"),
            smart_str(u"仰卧起坐评价"),
            smart_str(u"俯卧撑"),
            smart_str(u"俯卧撑评价"),
            smart_str(u"直身前屈"),
            smart_str(u"直身前屈评价"),
            smart_str(u"六分跑"),
            smart_str(u"六分跑评价"),
            smart_str(u"投掷"),
            smart_str(u"投掷评价"),
            smart_str(u"评价总分")
        ])
        for student in students:
            if check_student_error(student) != None:
                continue

            try:
                age = calculate_age(student.dateOfBirth, student.dateOfTesting)
            except:
                age = None

            try:
                month_age = calculate_monthdelta(student.dateOfBirth, student.dateOfTesting)
            except:
                month_age = None

            BMI = round(student.weight / (student.height * Decimal(0.01)) ** 2, 1)
            
            try:
                scoreItems = self.getscoreItems(student)
                remark = ''
                stand_score_sum = 0
                for scoreItem in scoreItems:
                    stand_score_sum += scoreItem.percentage * 100

                writer.writerow([
                    smart_str(student.lastName),
                    smart_str(student.firstName),
                    smart_str(student.schoolClass.school.name),
                    smart_str(str(student.schoolClass)),
                    smart_str(self.get_genderDisplay(student.gender)),
                    smart_str(student.dateOfBirth),
                    smart_str(student.dateOfTesting),
                    smart_str(age),
                    smart_str(month_age),
                    smart_str(remark),
                    smart_str(student.height),
                    smart_str(student.weight),
                    smart_str(BMI),
                    smart_str(scoreItems[0].original_score),
                    smart_str(scoreItems[0].percentage),
                    smart_str(scoreItems[1].original_score),
                    smart_str(scoreItems[1].percentage),
                    smart_str(scoreItems[2].original_score),
                    smart_str(scoreItems[2].percentage),
                    smart_str(scoreItems[3].original_score),
                    smart_str(scoreItems[3].percentage),
                    smart_str(scoreItems[4].original_score),
                    smart_str(scoreItems[4].percentage),
                    smart_str(scoreItems[5].original_score),
                    smart_str(scoreItems[5].percentage),
                    smart_str(scoreItems[6].original_score),
                    smart_str(scoreItems[6].percentage),
                    smart_str(scoreItems[7].original_score),
                    smart_str(scoreItems[7].percentage),
                    smart_str(scoreItems[8].original_score),
                    smart_str(scoreItems[8].percentage),
                    smart_str(stand_score_sum)
                    ])
            except Exception as e:
                remark = str(e)
                
                writer.writerow([
                    smart_str(student.lastName),
                    smart_str(student.firstName),
                    smart_str(student.schoolClass.school.name),
                    smart_str(str(student.schoolClass)),
                    smart_str(self.get_genderDisplay(student.gender)),
                    smart_str(student.dateOfBirth),
                    smart_str(student.dateOfTesting),
                    smart_str(age),
                    smart_str(month_age),
                    smart_str(remark),
                    smart_str(student.height),
                    smart_str(student.weight),
                    smart_str(BMI),
                    smart_str(student.e_bal),
                    None,
                    smart_str(student.e_shh),
                    None,
                    smart_str(student.e_sws),
                    None,
                    smart_str(student.e_20m),
                    None,
                    smart_str(student.e_su),
                    None,
                    smart_str(student.e_ls),
                    None,
                    smart_str(student.e_rb),
                    None,
                    smart_str(student.e_lauf),
                    None,
                    smart_str(student.e_ball),
                    None
                    ])
        return response

    def get_genderDisplay(self, genderName):
        if genderName == 'MALE':
            return '男'
        elif genderName == 'FEMALE':
            return '女'
        else:
            return genderName

    change_list_template = 'admin/sportsman/student/change_list.html'

class StudentCertificateScoreItem:
    percentage = 0.0
    original_score = 0.0
    unit = ''
    precision = 0
    def __init__(self,percentage, original_score, unit, precision = 0):
        self.percentage = percentage
        self.original_score = original_score
        self.unit = unit
        self.precision = precision

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户资料'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class StudentEvaluationAdmin(admin.ModelAdmin):
    list_display = ('noOfStudentStatus','district','lastName','firstName','school','schoolClass','gender','dateOfBirth','dateOfTesting','bmi','score_sum')
    list_filter = ('student__schoolClass__school__district','student__schoolClass__school')
    fields = ('lastName', 'firstName', 'school', 'schoolClass', 'gender', 'dateOfBirth', 'dateOfTesting', 'age', 'month_age', 'day_age', 'height', 'weight', 'bmi', 'original_score_bal', 'percentage_bal', 'original_score_shh', 'percentage_shh', 'original_score_sws', 'percentage_sws', 'original_score_20m', 'percentage_20m', 'original_score_su', 'percentage_su', 'original_score_ls', 'percentage_ls', 'original_score_rb', 'percentage_rb', 'original_score_lauf', 'percentage_lauf', 'original_score_ball', 'percentage_ball', 'score_sum')
    readonly_fields = fields

    def get_fields(self, request, obj=None):
        fields = list(super(StudentEvaluationAdmin, self).get_fields(request, obj))
        currentUser = request.user
        if currentUser.groups.filter(name='district_users').count() > 0:
            fields.remove('original_score_bal')
            fields.remove('original_score_shh')
            fields.remove('original_score_sws')
            fields.remove('original_score_20m')
            fields.remove('original_score_su')
            fields.remove('original_score_ls')
            fields.remove('original_score_rb')
            fields.remove('original_score_lauf')
            fields.remove('original_score_ball')
        return fields

    def get_queryset(self, request):
        queryset=super(StudentEvaluationAdmin, self).get_queryset(request)
        currentUser = request.user
        if currentUser.groups.filter(name='district_users').count() > 0:
            district = None
            try:
                userprofile = currentUser.userprofile
                if userprofile.district != None:
                    district = currentUser.userprofile.district
            except:
                pass
            if district != None:
                queryset=queryset.filter(student__schoolClass__school__district=district)
                
                districtStudentEvaluation = StudentEvaluation.objects.filter(student__schoolClass__school__district=district)

                studentEvaluations_low = districtStudentEvaluation.order_by('score_sum')[:15]
                if studentEvaluations_low.count() > 0:
                    studentEvaluation_score_sum_low_max = list(studentEvaluations_low)[-1].score_sum
                else:
                    studentEvaluation_score_sum_low_max = None

                studentEvaluations_high = districtStudentEvaluation.order_by('-score_sum')[:15]
                if studentEvaluations_high.count() > 0:
                    studentEvaluation_score_sum_high_min = list(studentEvaluations_high)[-1].score_sum
                else:
                    studentEvaluation_score_sum_high_min = None
                
                if studentEvaluation_score_sum_low_max != None and studentEvaluation_score_sum_high_min != None:
                    queryset = queryset.filter(Q(score_sum__gte=studentEvaluation_score_sum_high_min)|Q(score_sum__lte=studentEvaluation_score_sum_low_max))
            else:
                queryset=StudentEvaluation.objects.none()
        return queryset
    
    def noOfStudentStatus(self, obj):
        return obj.student.noOfStudentStatus
    noOfStudentStatus.short_description = '学籍号'
    def lastName(self, obj):
        return obj.student.lastName
    lastName.short_description = '姓'
    def firstName(self, obj):
        return obj.student.firstName
    firstName.short_description = '名'
    def district(self, obj):
        return obj.student.schoolClass.school.district
    district.short_description = '区县'
    def school(self, obj):
        return obj.student.schoolClass.school
    school.short_description = '学校'
    def schoolClass(self, obj):
        return obj.student.schoolClass
    schoolClass.short_description = '班级'
    def gender(self, obj):
        return self.get_genderDisplay(obj.student.gender)
    gender.short_description = '性别'
    def dateOfBirth(self, obj):
        return self.get_genderDisplay(obj.student.dateOfBirth)
    dateOfBirth.short_description = '出生日期'
    def dateOfTesting(self, obj):
        return self.get_genderDisplay(obj.student.dateOfTesting)
    dateOfTesting.short_description = '测试日期'
    def height(self, obj):
        return self.get_genderDisplay(obj.student.height)
    height.short_description = '身高'
    def weight(self, obj):
        return self.get_genderDisplay(obj.student.weight)
    weight.short_description = '体重'

    def get_genderDisplay(self, genderName):
        if genderName == 'MALE':
            return '男'
        elif genderName == 'FEMALE':
            return '女'
        else:
            return genderName
    

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'universalName', 'district')

class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('school', 'name', 'universalName')

class SequenceNumberAdmin(admin.ModelAdmin):
    list_display = ('code', 'value', 'prefix', 'suffix')
    ordering = ('code',)

class TestRefDataItemForm(forms.ModelForm):
    key = forms.ChoiceField(label='数据项',
         choices=BLANK_CHOICE_DASH + list(MovementTypeKeys))

class TestRefDataItemInline(admin.TabularInline):
    model = TestRefDataItem
    form = TestRefDataItemForm

def calculate_monthdelta(date1, date2):
    def is_last_day_of_the_month(date):
        days_in_month = calendar.monthrange(date.year, date.month)[1]
        return date.day == days_in_month
    imaginary_day_2 = 31 if is_last_day_of_the_month(date2) else date2.day
    monthdelta = (
        (date2.month - date1.month) +
        (date2.year - date1.year) * 12 +
        (-1 if date1.day > imaginary_day_2 else 0)
        )
    return monthdelta

def calculate_age(date1, date2):
    return date2.year - date1.year - ((date2.month, date2.day) < (date1.month, date1.day))

def calculate_daydelta(date1, date2):
    return (date2 - date1).days

def evaluate_for_summary_item_20m(testSummaryData):
    movement_type = '20m'
    testRefData = testSummaryData.test_ref_data
    testRefDataItems_20m = TestRefDataItem.objects.filter(test_ref_data=testRefData, movement_type=movement_type)
    factors_20m = Factor.objects.filter(movement_type=movement_type ,gender=testSummaryData.student.gender, month_age=testSummaryData.month_age)
    if testRefDataItems_20m.exists() and factors_20m.exists():
        testSummaryDataItem = TestSummaryDataItem(test_summary_data=testSummaryData, movement_type=movement_type)
        testSummaryDataItem.value = min([testRefDataItems_20m.get(key='20m_1').value, testRefDataItems_20m.get(key='20m_2').value])
        testSummaryDataItem.evaluate_date = timezone.now()
        factor_20m = factors_20m[0]
        testSummaryDataItem.evaluate_value = round(1 - scipy.stats.norm(factor_20m.mean, factor_20m.standard_deviation).cdf(testSummaryDataItem.value), 2)
        testSummaryDataItem.save()

def evaluate_for_summary_item_ls(testSummaryData):
    movement_type = 'ls'
    testRefData = testSummaryData.test_ref_data
    testRefDataItems_ls = TestRefDataItem.objects.filter(test_ref_data=testRefData, movement_type=movement_type)
    factors_ls = Factor.objects.filter(movement_type=movement_type ,gender=testSummaryData.student.gender, month_age=testSummaryData.month_age)
    if testRefDataItems_ls.exists() and factors_ls.exists():
        testSummaryDataItem = TestSummaryDataItem(test_summary_data=testSummaryData, movement_type=movement_type)
        testSummaryDataItem.value = testRefDataItems_ls.get(key='ls').value
        testSummaryDataItem.evaluate_date = timezone.now()
        factor_ls = factors_ls[0]
        testSummaryDataItem.evaluate_value = round(scipy.stats.norm(factor_ls.mean, factor_ls.standard_deviation).cdf(testSummaryDataItem.value), 2)
        testSummaryDataItem.save()    

class TestRefDataAdmin(admin.ModelAdmin):
    list_display = ('testing_date','testing_number','student', 'school_name')
    list_filter = ('student__school_name',)
    inlines = [
        TestRefDataItemInline,
    ]
    def school_name(self, obj):
        return obj.student.school_name
    school_name.short_description = '学校'
    school_name.admin_order_field = 'student__school_name'

class TestRefDataItemAdmin(admin.ModelAdmin):
    list_display = ('test_ref_data','movement_type','key', 'value')

class TestSummaryDataItemInline(admin.TabularInline):
    model = TestSummaryDataItem

class TestSummaryDataAdmin(admin.ModelAdmin):
    list_display = ('testing_date','student', 'month_age', 'school_name')
    list_filter = ('student__school_name',)
    inlines = [
        TestSummaryDataItemInline,
    ]
    def school_name(self, obj):
        return obj.student.school_name
    school_name.short_description = '学校'
    school_name.admin_order_field = 'student__school_name'


admin.site.register(SequenceNumber, SequenceNumberAdmin)
admin.site.register(StandardParameter,StandardParameterAdmin)
admin.site.register(Factor,FactorAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(SchoolClass, SchoolClassAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(StudentEvaluation,StudentEvaluationAdmin)
