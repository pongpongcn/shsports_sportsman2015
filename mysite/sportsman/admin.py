from django.contrib import admin
from django import forms
from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.db.models import Q
from django.db.models.fields import BLANK_CHOICE_DASH
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin, base_formats
from import_export.formats.base_formats import TextFormat
from import_export.instance_loaders import ModelInstanceLoader
import calendar, os, pinyin, json, csv, tempfile, zipfile
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
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable
from PyPDF2 import PdfFileWriter, PdfFileReader
from decimal import Decimal
from django.core.validators import *
from django.utils.encoding import smart_str
from django.contrib.auth import get_permission_codename
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.core.servers.basehttp import FileWrapper
from .utils.certificate_generator import CertificateGenerator

from .models import Factor
from .models import Student
from .models import StudentEvaluation
from .models import UserProfile
from .models import District
from .models import School
from .models import SchoolClass
from .models import SequenceNumber
from .models import Genders
from .models import StandardParameter
from .models import TestPlan

# Register your models here.

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


class StandardParameterResource(resources.ModelResource):
    class Meta:
        model = StandardParameter
        import_id_fields = ('version', 'gender','age','percentile')
        exclude = ('id',)

class StandardParameterAdmin(ImportExportModelAdmin):
    resource_class = StandardParameterResource
    list_display = ('version', 'gender', 'age', 'percentile', 'e_20m', 'e_bal', 'e_shh', 'e_rb', 'e_ls', 'e_su', 'e_sws', 'e_ball', 'e_lauf')
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
            'fields': ('testPlan', 'noOfStudentStatus', ('school', 'schoolClass'), ('firstName', 'lastName'), ('universalFirstName', 'universalLastName'), 'gender', 'dateOfBirth', ('dateOfTesting', 'number'))
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
    
    list_display = ('testPlan', 'noOfStudentStatus', 'lastName', 'firstName', 'gender', 'dateOfBirth', 'district', 'school', 'schoolClass', 'dateOfTesting', 'number', 'dataCompleted')
    list_display_links = ('noOfStudentStatus', 'lastName', 'firstName')
    list_filter = ('testPlan', 'dateOfTesting','schoolClass__school__district','schoolClass__school', StudentDataCompletedListFilter)
    ordering = ('testPlan', 'dateOfTesting', 'number')
    readonly_fields = ('external_id', 'school', 'number')
    search_fields = ('lastName', 'firstName', '=number', '=noOfStudentStatus')
    radio_fields = {"gender": admin.HORIZONTAL}
    list_select_related = True#性能优化

    def get_urls(self):
        urls = super(StudentAdmin, self).get_urls()
        my_urls = [
            url(r'^(.+)/gen_data_sheet_printable/$', self.admin_site.admin_view(self.gen_data_sheet_printable)),
            url(r'^gen_data_sheet_printable/$', self.admin_site.admin_view(self.gen_data_sheet_printables)),
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

    def gen_data_sheet_printable_response(self, students):
        pdfmetrics.registerFont(ttfonts.TTFont("simsun", "simsun.ttc"))
        pagesize = landscape(A4)
        fontName = 'simsun'

        output = PdfFileWriter()

        dictGenders = dict(Genders)

        templateImagePath = os.path.join(os.path.dirname(__file__), 'resources'+os.sep+'DataSheetTemplate.jpg')
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

        age = student.age
            
        standardParameters = StandardParameter.objects.filter(version=version, gender=student.gender, age=age)

        if not standardParameters.exists():
            raise Exception('数据异常: 没有适用的评分标准')

        scoreItems = []

        try:
            standardParameter_bal = standardParameters.filter(e_bal__lte=student.e_bal).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_bal.percentile*Decimal(0.01), student.e_bal, '步'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_bal, '步'))

        try:
            standardParameter_shh = standardParameters.filter(e_shh__lte=student.e_shh).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_shh.percentile*Decimal(0.01), student.e_shh, '次'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_shh, '次'))

        try:
            standardParameter_sws = standardParameters.filter(e_sws__lte=student.e_sws).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_sws.percentile*Decimal(0.01), student.e_sws, '厘米'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_sws, '厘米'))

        try:
            standardParameter_20m = standardParameters.filter(e_20m__gte=student.e_20m).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_20m.percentile*Decimal(0.01), student.e_20m, '秒', 2))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_20m, '秒', 2))

        try:
            standardParameter_su = standardParameters.filter(e_su__lte=student.e_su).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_su.percentile*Decimal(0.01), student.e_su, '重复次数'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_su, '重复次数'))

        try:
            standardParameter_ls = standardParameters.filter(e_ls__lte=student.e_ls).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_ls.percentile*Decimal(0.01), student.e_ls, '重复次数'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_ls, '重复次数'))

        try:
            standardParameter_rb = standardParameters.filter(e_rb__lte=student.e_rb).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_rb.percentile*Decimal(0.01), student.e_rb, '厘米'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_rb, '厘米'))

        try:
            standardParameter_lauf = standardParameters.filter(e_lauf__lte=student.e_lauf).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_lauf.percentile*Decimal(0.01), student.e_lauf, '米'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_lauf, '米'))

        try:
            standardParameter_ball = standardParameters.filter(e_ball__lte=student.e_ball).order_by('-percentile')[0]
            scoreItems.append(StudentCertificateScoreItem(standardParameter_ball.percentile*Decimal(0.01), student.e_ball, '米'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_ball, '米'))

        return scoreItems

    def getscoreItems_factor(self, student):
        version = 'for_china_by_chinese_at_201509'

        month_age = student.months_of_age

        factors = Factor.objects.filter(version=version, gender=student.gender, month_age=month_age)

        if not factors.exists():
            raise Exception('数据异常: 没有适用的评分标准')

        factor = factors[0]

        scoreItems = []

        try:
            mean = float(factor.mean_bal)
            standard_deviation = float(factor.standard_deviation_bal)
            original_score = float(student.e_bal)
            percentile = round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, student.e_bal, '步'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_bal, '步'))

        try:
            mean = float(factor.mean_shh)
            standard_deviation = float(factor.standard_deviation_shh)
            original_score = float(student.e_shh)
            percentile = round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, student.e_shh, '次'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_shh, '次'))

        try:
            mean = float(factor.mean_sws)
            standard_deviation = float(factor.standard_deviation_sws)
            original_score = float(student.e_sws)
            percentile = round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, student.e_sws, '厘米'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_sws, '厘米'))

        try:
            mean = float(factor.mean_20m)
            standard_deviation = float(factor.standard_deviation_20m)
            original_score = float(student.e_20m)
            percentile = 1- round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, student.e_20m, '秒', 2))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_20m, '秒', 2))

        try:
            mean = float(factor.mean_su)
            standard_deviation = float(factor.standard_deviation_su)
            original_score = float(student.e_su)
            percentile = round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, student.e_su, '重复次数'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_su, '重复次数'))

        try:
            mean = float(factor.mean_ls)
            standard_deviation = float(factor.standard_deviation_ls)
            original_score = float(student.e_ls)
            percentile = round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, student.e_ls, '重复次数'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_ls, '重复次数'))

        try:
            mean = float(factor.mean_rb)
            standard_deviation = float(factor.standard_deviation_rb)
            original_score = float(student.e_rb)
            percentile = round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, student.e_rb, '厘米'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_rb, '厘米'))

        try:
            mean = float(factor.mean_lauf)
            standard_deviation = float(factor.standard_deviation_lauf)
            original_score = float(student.e_lauf)
            percentile = round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, student.e_lauf, '米'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_lauf, '米'))

        try:
            mean = float(factor.mean_ball)
            standard_deviation = float(factor.standard_deviation_ball)
            original_score = float(student.e_ball)
            percentile = round(scipy.stats.norm(mean,standard_deviation).cdf(original_score), 2)
            scoreItems.append(StudentCertificateScoreItem(percentile, student.e_ball, '米'))
        except:
            scoreItems.append(StudentCertificateScoreItem(Decimal(0), student.e_ball, '米'))

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
                age = student.age
                month_age = student.months_of_age
                day_age = student.days_of_age
                
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

                studentEvaluation.e_bal = scoreItems[0].original_score
                studentEvaluation.p_bal = scoreItems[0].percentage
                studentEvaluation.e_shh = scoreItems[1].original_score
                studentEvaluation.p_shh = scoreItems[1].percentage
                studentEvaluation.e_sws = scoreItems[2].original_score
                studentEvaluation.p_sws = scoreItems[2].percentage
                studentEvaluation.e_20m = scoreItems[3].original_score
                studentEvaluation.p_20m = scoreItems[3].percentage
                studentEvaluation.e_su = scoreItems[4].original_score
                studentEvaluation.p_su = scoreItems[4].percentage
                studentEvaluation.e_ls = scoreItems[5].original_score
                studentEvaluation.p_ls = scoreItems[5].percentage
                studentEvaluation.e_rb = scoreItems[6].original_score
                studentEvaluation.p_rb = scoreItems[6].percentage
                studentEvaluation.e_lauf = scoreItems[7].original_score
                studentEvaluation.p_lauf = scoreItems[7].percentage
                studentEvaluation.e_ball = scoreItems[8].original_score
                studentEvaluation.p_ball = scoreItems[8].percentage
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

            age = student.age

            month_age = student.months_of_age

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
                    smart_str(student.get_gender_display()),
                    smart_str(student.dateOfBirth),
                    smart_str(student.dateOfTesting),
                    smart_str(age),
                    smart_str(month_age),
                    smart_str(remark),
                    smart_str(student.height),
                    smart_str(student.weight),
                    smart_str(BMI),
                    smart_str(student.e_bal),
                    smart_str(scoreItems[0].percentage),
                    smart_str(student.e_shh),
                    smart_str(scoreItems[1].percentage),
                    smart_str(student.e_sws),
                    smart_str(scoreItems[2].percentage),
                    smart_str(student.e_20m),
                    smart_str(scoreItems[3].percentage),
                    smart_str(student.e_su),
                    smart_str(scoreItems[4].percentage),
                    smart_str(student.e_ls),
                    smart_str(scoreItems[5].percentage),
                    smart_str(student.e_rb),
                    smart_str(scoreItems[6].percentage),
                    smart_str(student.e_lauf),
                    smart_str(scoreItems[7].percentage),
                    smart_str(student.e_ball),
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
                    smart_str(student.get_gender_display()),
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

class StudentEvaluationAdmin(admin.ModelAdmin):
    list_display = ('testPlan','noOfStudentStatus','district','lastName','firstName','school','schoolClass','gender','is_talent','is_frail')
    list_filter = ('testPlan','student__schoolClass__school__district','student__gender','is_talent','is_frail')
    fields = ('testPlan','lastName', 'firstName', 'school', 'schoolClass', 'gender', 'dateOfBirth', 'dateOfTesting', 'age', 'months_of_age', 'days_of_age', 'height', 'weight', 'bmi', 'e_bal', 'p_bal', 'e_shh', 'p_shh', 'e_sws', 'p_sws', 'e_20m', 'p_20m', 'e_su', 'p_su', 'e_ls', 'p_ls', 'e_rb', 'p_rb', 'e_lauf', 'p_lauf', 'e_ball', 'p_ball', 'certificate_file')
    ordering = ('student__schoolClass__school__district', 'student__schoolClass__school', 'student__schoolClass', 'student__lastName', 'student__firstName')
    
    temp_readonly_fields = list(fields)
    temp_readonly_fields.remove('certificate_file')
    readonly_fields = tuple(temp_readonly_fields)

    def get_urls(self):
        urls = super(StudentEvaluationAdmin, self).get_urls()
        my_urls = [
            url(r'^(.+)/gen_certificate_printable/$', self.admin_site.admin_view(self.gen_certificate_printable)),
            url(r'^gen_certificate_printable/$', self.admin_site.admin_view(self.gen_certificate_printables)),
        ]
        return my_urls + urls 
    
    #对于区县控制显示内容的代码见Rev.201
    def get_fields(self, request, obj=None):
        fields = list(super(StudentEvaluationAdmin, self).get_fields(request, obj))
        currentUser = request.user
        if currentUser.groups.filter(name='district_users').count() > 0:
            fields.remove('e_bal')
            fields.remove('e_shh')
            fields.remove('e_sws')
            fields.remove('e_20m')
            fields.remove('e_su')
            fields.remove('e_ls')
            fields.remove('e_rb')
            fields.remove('e_lauf')
            fields.remove('e_ball')
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
    lastName.admin_order_field = 'student__lastName'
    def firstName(self, obj):
        return obj.student.firstName
    firstName.short_description = '名'
    firstName.admin_order_field = 'student__firstName'
    def district(self, obj):
        return obj.student.schoolClass.school.district
    district.short_description = '区县'
    district.admin_order_field = 'student__schoolClass__school__district'
    def school(self, obj):
        return obj.student.schoolClass.school
    school.short_description = '学校'
    school.admin_order_field = 'student__schoolClass__school'
    def schoolClass(self, obj):
        return obj.student.schoolClass
    schoolClass.short_description = '班级'
    schoolClass.admin_order_field = 'student__schoolClass'
    def gender(self, obj):
        return obj.student.get_gender_display()
    gender.short_description = '性别'
    def dateOfBirth(self, obj):
        return obj.student.dateOfBirth
    dateOfBirth.short_description = '出生日期'
    def dateOfTesting(self, obj):
        return obj.student.dateOfTesting
    dateOfTesting.short_description = '测试日期'
    def height(self, obj):
        return obj.student.height
    height.short_description = '身高'
    def weight(self, obj):
        return obj.student.weight
    weight.short_description = '体重'
    def e_bal(self, obj):
        return obj.student.e_bal
    e_bal.short_description = '平衡'
    def e_shh(self, obj):
        return obj.student.e_shh
    e_shh.short_description = '侧向跳'
    def e_sws(self, obj):
        return obj.student.e_sws
    e_sws.short_description = '跳远'
    def e_20m(self, obj):
        return obj.student.e_20m
    e_20m.short_description = '20米冲刺跑'
    def e_su(self, obj):
        return obj.student.e_su
    e_su.short_description = '仰卧起坐'
    def e_ls(self, obj):
        return obj.student.e_ls
    e_ls.short_description = '俯卧撑'
    def e_rb(self, obj):
        return obj.student.e_rb
    e_rb.short_description = '直身前屈'
    def e_lauf(self, obj):
        return obj.student.e_lauf
    e_lauf.short_description = '六分跑'
    def e_ball(self, obj):
        return obj.student.e_ball
    e_ball.short_description = '投掷'
    def age(self, obj):
        return obj.student.age
    age.short_description = '年龄'
    def months_of_age(self, obj):
        return obj.student.months_of_age
    months_of_age.short_description = '月龄'
    def days_of_age(self, obj):
        return obj.student.days_of_age
    days_of_age.short_description = '日龄'
    def bmi(self, obj):
        return obj.student.bmi
    bmi.short_description = 'BMI'

    def gen_certificate_printable(self, request, object_id):
        studentEvaluation = StudentEvaluation.objects.get(pk=object_id)
        
        return self._gen_certificate((studentEvaluation,))
    
    def gen_certificate_printables(self, request, *args, **kwargs):
        studentEvaluations = self.get_student_evaluation_queryset(request)
        
        return self._gen_certificate(studentEvaluations)

    def _gen_certificate(self, studentEvaluations):
        '''
        输出PDF内容到临时文件，随后分段发送到客户端。
        从而避免内存过多消耗，同时临时文件会自动移除。
        '''
        
        fp = tempfile.TemporaryFile()
        
        generator = CertificateGenerator(fp)
        
        generator.build(studentEvaluations)
        
        filesize = fp.tell()
        fp.seek(0)
        
        if len(studentEvaluations) == 1:
            studentEvaluation = studentEvaluations[0]
            filename = 'Certificate.pdf'
        else:
            filename = 'Certificates.pdf'
        
        response = StreamingHttpResponse(FileWrapper(fp), content_type='application/pdf')
        response['Content-Length'] = filesize
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        
        return response
    
    def get_student_evaluation_queryset(self, request):
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

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'universalName', 'district')

class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('school', 'name', 'universalName')
    
class TestPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'startDate', 'endDate', 'isPublished')

class SequenceNumberAdmin(admin.ModelAdmin):
    list_display = ('code', 'value', 'prefix', 'suffix')
    ordering = ('code',)

admin.site.register(SequenceNumber, SequenceNumberAdmin)
admin.site.register(StandardParameter,StandardParameterAdmin)
admin.site.register(Factor,FactorAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(SchoolClass, SchoolClassAdmin)
admin.site.register(TestPlan, TestPlanAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(StudentEvaluation,StudentEvaluationAdmin)