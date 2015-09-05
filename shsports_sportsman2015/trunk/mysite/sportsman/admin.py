from django.contrib import admin

from .models import Factor
from .models import Student

# Register your models here.

class FactorAdmin(admin.ModelAdmin):
    list_display = ('gender', 'month_age', 'movement_type', 'mean', 'standard_deviation')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'gender', 'dateOfBirth', 'schoolName', 'className')

admin.site.register(Factor,FactorAdmin)
admin.site.register(Student,StudentAdmin)
