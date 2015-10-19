from django.contrib import admin
from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from import_export import resources
from import_export import fields
from import_export.admin import ImportExportModelAdmin
import calendar
from django.utils import timezone
from statistics import mean
import scipy.stats

from .models import Factor
from .models import Student
from .models import TestRefData
from .models import TestRefDataItem
from .models import TestSummaryData
from .models import TestSummaryDataItem
from .models import School
from .models import SchoolClass

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

class FactorResource(resources.ModelResource):
    class Meta:
        model = Factor
        import_id_fields = ('gender','month_age','movement_type')
        exclude = ('id')

class FactorAdmin(ImportExportModelAdmin):
    resource_class = FactorResource
    list_display = ('movement_type', 'gender', 'month_age', 'mean', 'standard_deviation')
    list_filter = ('movement_type', 'gender', 'month_age')

class StudentResource(resources.ModelResource):
    id = fields.Field(attribute='external_id')
    firstName = fields.Field(attribute='first_name')
    lastName = fields.Field(attribute='last_name')
    dateOfBirth = fields.Field(attribute='birth_date')
    schoolName = fields.Field(attribute='school_name')
    className = fields.Field(attribute='class_name')
    class Meta:
        model = Student
        import_id_fields = ('id',)
        fields = ('gender',)
        exclude = ('id')

class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    date_hierarchy = 'dateOfTesting'
    #fields = ('schoolClass', ('firstName', 'lastName'), ('universalFirstName', 'universalLastName'), 'gender', 'dateOfBirth', ('dateOfTesting', 'number'), 'questionary', ('street', 'housenumber'), 'addition', ('zip', 'city'), 'addressClearance', ('e_20m_1', 'e_20m_2'), ('e_bal30_1', 'e_bal30_2', 'e_bal45_1', 'e_bal45_2', 'e_bal60_1', 'e_bal60_2'), ('e_ball_1', 'e_ball_2', 'e_ball_3'), ('e_lauf_rest', 'e_lauf_runden'), 'e_ls', ('e_rb_1', 'e_rb_2'), ('e_shh_1f', 'e_shh_1s', 'e_shh_2f', 'e_shh_2s'), 'e_slauf_10', 'e_su', ('e_sws_1', 'e_sws_2'), ('weight', 'height'))
    fieldsets = (
        (None, {
            'fields': ('schoolClass', 'firstName', 'lastName', 'universalFirstName', 'universalLastName', 'gender')
        }),
        ('地址', {
            'classes': ('wide',),
            'description': 'It\' a description.',
            'fields': (('street', 'housenumber'), 'addition', ('zip', 'city'))
        })
    )

    def school(student):
        return student.schoolClass.school
    school.short_description = '学校'
    school.admin_order_field = 'schoolClass__school'
    
    list_display = ('lastName', 'firstName', 'dateOfBirth', school, 'schoolClass', 'dateOfTesting', 'number')
    list_filter = ('dateOfTesting',)
    ordering = ('dateOfTesting', 'number')
    readonly_fields = ('external_id',)
    list_select_related = True#性能优化

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'universalName')

class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('school', 'name', 'universalName')

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

def evaluate_for_summary(modeladmin, request, queryset):
    for testRefData in queryset:
        testSummaryDataQuery = TestSummaryData.objects.filter(test_ref_data=testRefData)
        if testSummaryDataQuery.exists():
            testSummaryData = testSummaryDataQuery[0]
        else:
            testSummaryData = TestSummaryData(test_ref_data=testRefData, student=testRefData.student, testing_date=testRefData.testing_date, height=testRefData.height, weight=testRefData.weight)
            delta_age = testRefData.testing_date - testRefData.student.birth_date
            testSummaryData.month_age = calculate_monthdelta(testRefData.student.birth_date, testRefData.testing_date)
            testSummaryData.day_age = delta_age.days
            testSummaryData.save()

        TestSummaryDataItem.objects.filter(test_summary_data=testSummaryData).delete()
        #20米冲刺跑
        evaluate_for_summary_item_20m(testSummaryData)
        #俯卧撑
        evaluate_for_summary_item_ls(testSummaryData)
        
evaluate_for_summary.short_description = "评估"

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
    actions = [evaluate_for_summary]
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


admin.site.register(School, SchoolAdmin)
admin.site.register(SchoolClass, SchoolClassAdmin)
admin.site.register(Factor,FactorAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(TestRefData,TestRefDataAdmin)
admin.site.register(TestRefDataItem,TestRefDataItemAdmin)
admin.site.register(TestSummaryData,TestSummaryDataAdmin)
admin.site.register(TestSummaryDataItem)
