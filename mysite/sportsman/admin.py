from django.contrib import admin

from .models import Factor
from .models import Student
from .models import TestRefData
from .models import TestRefDataItem
from .models import TestSummaryData
from .models import TestSummaryDataItem

# Register your models here.

class FactorAdmin(admin.ModelAdmin):
    list_display = ('gender', 'month_age', 'movement_type', 'mean', 'standard_deviation')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'gender', 'dateOfBirth', 'schoolName', 'className')
    list_filter = ('gender', 'dateOfBirth', 'schoolName')

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
