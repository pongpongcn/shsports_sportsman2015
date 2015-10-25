from django.contrib import admin
from django import forms
from django.conf.urls import url
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models.fields import BLANK_CHOICE_DASH
from import_export import resources
from import_export import fields
from import_export.admin import ImportExportModelAdmin
import calendar, random
from django.utils import timezone
from statistics import mean
import scipy.stats
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts
from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape, letter
from reportlab.lib.units import cm, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, BaseDocTemplate, Frame, PageBreak, PageTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.tables import TableStyle
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib import colors
from PyPDF2 import PdfFileWriter, PdfFileReader

from .models import Factor
from .models import Student
from .models import TestRefData
from .models import TestRefDataItem
from .models import TestSummaryData
from .models import TestSummaryDataItem
from .models import School
from .models import SchoolClass
from .models import SequenceNumber
from .models import Genders

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
    e_sws_1 = fields.Field()
    e_sws_2 = fields.Field()
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
    
    class Meta:
        model = Student
        #import_id_fields = ('id',)
        fields = ('id','firstName','lastName','universalFirstName','universalLastName','street','housenumber','addition','zip','city','gender','questionary','number','weight','height','dateOfBirth','dateOfTesting','e_20m_1','e_20m_2','e_bal60_1','e_bal60_2','e_bal45_1','e_bal45_2','e_bal30_1','e_bal30_2','e_shh_1s','e_shh_1f','e_shh_2s','e_shh_2f','e_rb_1','e_rb_2','e_ls','e_su','e_ball_1','e_ball_2','e_ball_3','e_lauf_runden','e_lauf_rest','e_slauf_10')
        #fields = ('id','firstName','lastName','universalFirstName','universalLastName','street','housenumber','addition','zip','city','gender','questionary','number','numberTalentCheck','weight','height','dateOfBirth','dateOfTesting','dateOfTalentCheck','selectedForTalentCheck','addressClearance','e_20m_1','e_20m_2','e_20m','e_bal60_1','e_bal60_2','e_bal45_1','e_bal45_2','e_bal30_1','e_bal30_2','e_bal','e_shh_1s','e_shh_1f','e_shh_2s','e_shh_2f','e_shh','e_rb_1','e_rb_2','e_rb','e_ls','e_su','e_sws_1','e_sws_2','e_sws','e_ball_1','e_ball_2','e_ball_3','e_ball','e_lauf_runden','e_lauf_rest','e_lauf','comment','e_15m_sw','e_15m_sw_bbs','e_15m_sw_ns','e_10m_ped_1','e_10m_ped_2','e_10m_ped','e_slauf_10','e_tt_15s_1','e_tt_15s_2','e_tt_15s','e_fb_drib_ob_1','e_fb_drib_ob_2','e_fb_drib_ob','e_fb_drib_mb_1','e_fb_drib_mb_2','e_fb_drib_mb','z_20m','z_bal','z_shh','z_rb','z_sws','z_ball','z_lauf','z_ls','z_su','z_10m_ped','z_15m_sw','z_fb_drib_mb','z_fb_drib_ob','z_tt_15s','z_slauf_10','z_height','z_weight','z_bmi','p_20m','p_bal','p_shh','p_rb','p_ls','p_su','p_sws','p_ball','p_lauf','p_height','p_weight','p_bmi','p_10m_ped','p_15m_sw','p_fb_drib_mb','p_fb_drib_ob','p_tt_15s','p_slauf_10',)
        #exclude = ('id')
    #'className','universalClassName','schoolName','universalSchoolName',
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

class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    date_hierarchy = 'dateOfTesting'
    fieldsets = (
        (None, {
            'fields': (('school', 'schoolClass'), ('firstName', 'lastName'), ('universalFirstName', 'universalLastName'), 'gender', 'dateOfBirth', ('dateOfTesting', 'number'), 'questionary')
            }),
        ('地址', {
            'classes': ('wide',),
            'fields': (('street', 'housenumber'), 'addition', ('zip', 'city'))
            }),
        ('测试成绩', {
            'classes': ('collapse',),
            'description': '正常情况下不要在此处编辑这些数据。',
            'fields': ('addressClearance', ('weight', 'height'), ('e_20m_1', 'e_20m_2'), ('e_bal30_1', 'e_bal30_2', 'e_bal45_1', 'e_bal45_2', 'e_bal60_1', 'e_bal60_2'), ('e_ball_1', 'e_ball_2', 'e_ball_3'), ('e_lauf_rest', 'e_lauf_runden'), 'e_ls', ('e_rb_1', 'e_rb_2'), ('e_shh_1f', 'e_shh_1s', 'e_shh_2f', 'e_shh_2s'), 'e_slauf_10', 'e_su', ('e_sws_1', 'e_sws_2'))
            }),
        ('其它', {
            'classes': ('collapse',),
            'fields': ('external_id',)
            })
    )

    def school(self, instance):
        return instance.schoolClass.school
    school.short_description = '学校'
    school.admin_order_field = 'schoolClass__school'
    
    list_display = ('lastName', 'firstName', 'gender', 'dateOfBirth', 'school', 'schoolClass', 'dateOfTesting', 'number')
    list_display_links = ('lastName', 'firstName')
    list_filter = ('dateOfTesting','schoolClass__school')
    ordering = ('dateOfTesting', 'number')
    readonly_fields = ('external_id', 'school', 'number')
    search_fields = ('lastName', 'firstName')
    radio_fields = {"gender": admin.HORIZONTAL}
    list_select_related = True#性能优化

    def get_urls(self):
        urls = super(StudentAdmin, self).get_urls()
        my_urls = [
            url(r'^(.+)/gen_data_sheet_printable/$', self.admin_site.admin_view(self.gen_data_sheet_printable)),
            url(r'^gen_data_sheet_printable/$', self.admin_site.admin_view(self.gen_data_sheet_printables)),
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
        
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

        filename = 'Data Sheets' + '.pdf'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + filename +'"'

        buffer = BytesIO()

        # Create the PDF object, using the response object as its "file."
        pagesize = landscape(A4)

        styles=getSampleStyleSheet()

        doc = BaseDocTemplate(buffer,pagesize=pagesize,leftMargin=1*cm,rightMargin=1*cm,topMargin=1*cm,bottomMargin=1*cm)

        Story = []

        columnWidth = doc.width/2-6
        #Two Columns
        frame1 = Frame(doc.leftMargin, doc.bottomMargin, columnWidth, doc.height, id='col1')
        frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, columnWidth, doc.height, id='col2')

        #Story.append(Paragraph(" ".join([random.choice(words) for i in range(1000)]),styles['Normal']))
        doc.addPageTemplates([PageTemplate(id='TwoCol',frames=[frame1,frame2]), ])
        
        styles = getSampleStyleSheet()
        styles["Normal"].fontName='STSong-Light'
        styles.add(ParagraphStyle(name='Student-Info', fontName='STSong-Light'))
        styles.add(ParagraphStyle(name='Data-Info', fontName='STSong-Light'))

        for student in students:
            Story.extend(self.gen_data_sheet_printable_single_page(student, styles, columnWidth))
            Story.append(PageBreak())

        doc.build(Story)

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    
    def gen_data_sheet_printable(self, request, object_id):
        student = Student.objects.get(pk=object_id)
        
        return self.gen_data_sheet_printable_response((student,))

    def gen_data_sheet_printable_response(self, students):
        pdfmetrics.registerFont(ttfonts.TTFont("simsun", "simsun.ttc"))
        pagesize = landscape(A4)
        fontName = 'simsun'

        output = PdfFileWriter()
        
        for student in students:
            # create a new PDF with Reportlab
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=pagesize)
            p.setFont("simsun", 14)
            p.drawString(0, 0, '%s, %s' % (student.lastName, student.firstName))
            p.save()
            buffer.seek(0)
            new_pdf = PdfFileReader(buffer)
            # read your existing PDF
            existing_pdf = PdfFileReader(open("test.pdf", "rb"))
            # add the "watermark" (which is the new pdf) on the existing page
            
            page = existing_pdf.getPage(0)
            page.mergePage(new_pdf.getPage(0))
            output.addPage(page)

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
            
        # finally, write "output" to a real file(response)
        output.write(response)

        return response    

    def gen_data_sheet_printable_single_page(self, student, styles, available_width):
        story = []

        studentInfoParagraphs = {}
        studentInfoParagraphs["title"] = Paragraph('<para alignment="center"><font size=16><b>2015 上海运动机能测试-数据管理表</b></font></para>',styles["Student-Info"])
        studentInfoParagraphs["name"] = Paragraph('<font size=14><b>姓, 名: </b>'+student.lastName+', '+student.firstName+'</font>',styles["Student-Info"])
        if student.universalLastName and student.universalFirstName:
            studentInfoParagraphs["universalName"] = Paragraph('<font size=14>'+student.universalLastName+', '+student.universalFirstName+'</font>',styles["Student-Info"])
        else:
            studentInfoParagraphs["universalName"] = None
        studentInfoParagraphs["number"] = Paragraph('<font size=14>'+'<b>测试编号: </b>'+str(student.number)+'</font>',styles["Student-Info"])
        if student.gender:
            genderString = dict(Genders)[student.gender]
        else:
            genderString = ''
         
        studentInfoParagraphs["gender"] = Paragraph('<b>性别: </b>'+genderString,styles["Student-Info"])
        studentInfoParagraphs["dateOfBirth"] = Paragraph('<b>出生年月: </b>'+str(student.dateOfBirth),styles["Student-Info"])
        studentInfoParagraphs["school"] = Paragraph('<b>学校: </b>'+student.schoolClass.school.universalName,styles["Student-Info"])
        studentInfoParagraphs["class"] = Paragraph('<b>班级: </b>'+str(student.schoolClass),styles["Student-Info"])
        studentInfoParagraphs["dateOfTesting"] = Paragraph('<b>测试日期: </b>'+str(student.dateOfTesting),styles["Student-Info"])
        
        data= [[studentInfoParagraphs["title"]],
               [studentInfoParagraphs["name"], studentInfoParagraphs["universalName"], studentInfoParagraphs["number"]],
               [studentInfoParagraphs["gender"], studentInfoParagraphs["dateOfBirth"]],
               [studentInfoParagraphs["school"]],
               [studentInfoParagraphs["class"]],
               [studentInfoParagraphs["dateOfTesting"]]]
        t=Table(data)
        t.setStyle(TableStyle([
            ('BOX', (0,0),(2,5),1,colors.black),
            ('SPAN',(0,0),(2,0)),
            ('SPAN',(0,3),(2,3))
            ]))
        t._argW[0]=4.5*cm
        t._argW[1]=4.5*cm
        story.append(t)

        story.append(Paragraph('测试日期&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;身高□□□厘米&nbsp;体重□□.□公斤&nbsp;号码□□□', styles["Data-Info"]))
        story.append(Paragraph('测试1: 20米跑',styles["Data-Info"]))
        story.append(Paragraph('第一次跑□.□□秒&nbsp;&nbsp;&nbsp;&nbsp;第二次跑□.□□秒',styles["Data-Info"]))
        story.append(Paragraph('测试2: 后退平衡',styles["Data-Info"]))
        story.append(Paragraph('1.&nbsp;6.0厘米&nbsp;最多8步&nbsp;&nbsp;第一次□ 第二次□',styles["Data-Info"]))
        
        return story
    
    def gen_data_sheet_printable_single_page_back(self, student, canvas, pagesize):
        canvas.saveState()
        #canvas.setFont("STSong-Light", 14)
        
        styleSheet = getSampleStyleSheet()
        styleSheet.add(ParagraphStyle(name='body', fontName='STSong-Light'))
        P=Paragraph('<para>This is a very silly example 中文</para>',styleSheet["body"])
        
        aW = 12.1*cm # available width and height
        aH = 5.8*cm
        w,h = P.wrap(aW, aH) # find required space
        P.drawOn(canvas,2.4*cm,pagesize[1]-1.5*cm)
        aH = aH - h # reduce the available height

        base_info_part_width = 12.1*cm
        base_info_part_height = 5.8*cm
        base_info_part_margin_x = 2.4*cm
        base_info_part_margin_y = pagesize[1]-1.5*cm-base_info_part_height
        
        canvas.rect(base_info_part_margin_x, base_info_part_margin_y, base_info_part_width, base_info_part_height)

        title = "2015 上海运动机能测试-数据管理表"
        title_padding_x = (base_info_part_width-canvas.stringWidth(title))/2
        if title_padding_x <0:
            title_padding_x = 0
        canvas.drawString(base_info_part_margin_x+title_padding_x, base_info_part_margin_y+3.8*cm, title)
        
        canvas.drawString(100, 100, "姓, 名: " + student.lastName + ', ' + student.firstName)
        canvas.drawString(0, 0, str(canvas.stringWidth("xxx")))
        canvas.rotate(90)
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        canvas.drawString(100, -100, "旋转90度")
        canvas.restoreState()

    change_form_template = 'sportsman/student_change_form.html'
    change_list_template = 'sportsman/student_list.html'

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'universalName')

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


admin.site.register(SequenceNumber, SequenceNumberAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(SchoolClass, SchoolClassAdmin)
admin.site.register(Factor,FactorAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(TestRefData,TestRefDataAdmin)
admin.site.register(TestRefDataItem,TestRefDataItemAdmin)
admin.site.register(TestSummaryData,TestSummaryDataAdmin)
admin.site.register(TestSummaryDataItem)
