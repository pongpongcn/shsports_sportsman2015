from django.contrib import admin
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

class TestRefDataAdmin(admin.ModelAdmin):
    list_display = ('testing_date','testing_number','student')

class TestRefDataItemAdmin(admin.ModelAdmin):
    list_display = ('test_ref_data','movement_type','key', 'value')

admin.site.register(Factor,FactorAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(TestRefData,TestRefDataAdmin)
admin.site.register(TestRefDataItem,TestRefDataItemAdmin)
admin.site.register(TestSummaryData)
admin.site.register(TestSummaryDataItem)
