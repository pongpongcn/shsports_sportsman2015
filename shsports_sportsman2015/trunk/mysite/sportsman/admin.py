from django.contrib import admin
from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from import_export import resources
from import_export import fields
from import_export.admin import ImportExportModelAdmin

from .models import Factor
from .models import Student
from .models import TestRefData
from .models import TestRefDataItem
from .models import TestSummaryData
from .models import TestSummaryDataItem

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
    def get_or_init_instance(self, instance_loader, row):
        #row['dateOfBirth'].pop()
        return super(StudentResource, self).get_or_init_instance(instance_loader, row)

class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = ('last_name', 'first_name', 'gender', 'birth_date', 'school_name', 'class_name')
    list_filter = ('gender', 'birth_date', 'school_name')
    readonly_fields = ('external_id',)

'''
class TestRefDataItemForm(forms.ModelForm):
    class Meta:
        model = TestRefDataItem
        fields = ('movement_type', 'key', 'value')
        widgets = {
            'key': forms.ChoiceField(choices=BLANK_CHOICE_DASH + list(MovementTypeKeys)),
            #'key': forms.Textarea(attrs={'placeholder': u'Bla bla'}),
        }
'''

class TestRefDataItemForm(forms.ModelForm):
    key = forms.ChoiceField(label='数据项',
         choices=BLANK_CHOICE_DASH + list(MovementTypeKeys))

class TestRefDataItemInline(admin.TabularInline):
    model = TestRefDataItem
    form = TestRefDataItemForm

class TestRefDataAdmin(admin.ModelAdmin):
    list_display = ('testing_date','testing_number','student')
    inlines = [
        TestRefDataItemInline,
    ]

class TestRefDataItemAdmin(admin.ModelAdmin):
    list_display = ('test_ref_data','movement_type','key', 'value')

admin.site.register(Factor,FactorAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(TestRefData,TestRefDataAdmin)
admin.site.register(TestRefDataItem,TestRefDataItemAdmin)
admin.site.register(TestSummaryData)
admin.site.register(TestSummaryDataItem)
