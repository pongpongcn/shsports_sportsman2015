from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, BaseDocTemplate, Frame, PageBreak, PageTemplate, Table, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import cm, inch
from reportlab.lib.fonts import tt2ps
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable, DocAssign
from reportlab.platypus.doctemplate import FrameBreak
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.barcharts import VerticalBarChart, HorizontalBarChart
from reportlab.graphics.charts.textlabels import LabelOffset

import os, json
from io import BytesIO
from reportlab.lib import colors
from decimal import Decimal

pdfmetrics.registerFont(TTFont('Microsoft-YaHei', 'MSYH.TTC'))
pdfmetrics.registerFont(TTFont('Microsoft-YaHei-Bold', 'MSYHBD.TTC'))
pdfmetrics.registerFont(TTFont('Microsoft-YaHei-Light', 'MSYHL.TTC'))
pdfmetrics.registerFontFamily('Microsoft-YaHei',normal='Microsoft-YaHei',bold='Microsoft-YaHei-Bold')
pdfmetrics.registerFontFamily('Microsoft-YaHei-Light',normal='Microsoft-YaHei-Light',bold='Microsoft-YaHei-Bold')

class CertificateGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.styles = getShanghaiMovementCheck2015StyleSheet()
    
    def build(self, studentEvaluations):
        doc = ShanghaiMovementCheck2015DocTemplate(self.filename)
        
        Story = []
        
        styles = self.styles
        
        for studentEvaluation in studentEvaluations:
            testPlanName = studentEvaluation.testPlan.name
            
            Story.append(FrameBreak('Header'))
            
            Story.append(Paragraph('证书', self.styles['Title']))
            Story.append(Paragraph(testPlanName, self.styles['Subtitle']))

            Story.append(FrameBreak('Content'))
            
            pdfStudentBasicInfo = PdfStudentBasicInfo(studentEvaluation, style=styles['Normal'])
            Story.append(pdfStudentBasicInfo)
            
            Story.append(Spacer(0,0.5*cm))
            
            p = Paragraph('您在%s中的表现' % testPlanName, styles['Normal'])
            Story.append(p)
            
            Story.append(Spacer(0,0.5*cm))
            
            pdfStudentPRChart = get_studentPRChart(studentEvaluation)
            Story.append(pdfStudentPRChart)
            
            Story.append(Spacer(0,1*cm))
            
            p = Paragraph('50%表示同年龄段孩子所具备运动能力的平均水平，百分比值越高代表孩子具备的运动能力越突出。百分比只是运动能力的参考值。', styles['Normal'])
            Story.append(p)
            
            Story.append(Spacer(0,0.5*cm))
            
            p = Paragraph('尊敬的家长：<br/>感谢您的孩子参加了我们的运动能力测试！<br/>您的孩子正处于各项身体素质发展的关键敏感期。这个阶段也是传统意义上的儿童体育运动阶段。让孩子参加到各种儿童体育运动中去，将为孩子运动机能的全面发展提供重要的机会。跳、跑、踢、抛、接、滑动、转动等能力，如果得到综合的运用和锻炼，将使孩子的手、眼、脑、四肢、肌肉、神经、心理得到均衡发展，并使您的孩子茁壮成长。', styles['Normal'])
            Story.append(p)
            
            Story.append(Spacer(0,0.5*cm))
            
            pdfStudentComment = PdfStudentComment(studentEvaluation, style=styles['Normal'])
            Story.append(pdfStudentComment)
            
            Story.append(FrameBreak('Signature'))
            p = Paragraph('''上海市青少年体育选材育才中心&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shanghai Sports Talent Identification & Development Center<br/>德国拜罗伊特大学&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;University of Bayreuth - Training & Movement Science''', styles['Normal'])
            Story.append(p)
            
            Story.append(PageBreak())

        doc.build(Story)
        
def get_studentPRChart(studentEvaluation):   
    pr_items = _get_pr_items(studentEvaluation)

    row_data = []
    row_barLabel = []
    categories = []
    
    '''这是一个Hack，因为Chart绘制的顺序和预期的不同。'''
    pr_items = reversed(pr_items)
    
    for item in pr_items:
        row_data.append(item.p_value)
        row_barLabel.append('%s%%(%s %s)' % (item.p_value, item.e_value, item.e_unit))
        categories.append(item.name)
        
    data = [row_data]
    labels = [row_barLabel]
    
    drawing = Drawing(14*cm, 6*cm)        
    bc = HorizontalBarChart()
    bc.x = 1.5*cm
    bc.y = 0
    bc.width = drawing.width - bc.x
    bc.height = drawing.height
    bc.data = data
    bc.bars.strokeColor = None
    bc.bars[0].fillColor = colors.HexColor('#7fd8ff')
    bc.barLabelFormat = 'values'
    bc.barLabelArray = labels
    bc.barLabels.boxAnchor = 'w'
    bc.barLabels.fixedEnd = LabelOffset()
    bc.barLabels.fixedEnd.posMode='low'
    
    bc.barLabels.fontName = 'Microsoft-YaHei-Light'
    bc.barLabels.fontSize = 8
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 100
    bc.valueAxis.valueStep = 10
    bc.valueAxis.labels.fontName = 'Microsoft-YaHei-Light'
    bc.valueAxis.labels.fontSize = 8
    bc.categoryAxis.categoryNames = categories
    bc.categoryAxis.labels.boxAnchor = 'w'
    bc.categoryAxis.labels.dx = -1.5*cm
    bc.categoryAxis.labels.fontName = 'Microsoft-YaHei-Light'
    bc.categoryAxis.labels.fontSize = 8
    bc.categoryAxis.visibleAxis = 0
    bc.categoryAxis.visibleTicks = 0

    drawing.add(bc)
    
    return drawing
    
def _get_pr_items(studentEvaluation):
    pr_items = []
    pr_items.append(PRItem('平衡', studentEvaluation.student.e_bal, '步', studentEvaluation.p_bal))
    pr_items.append(PRItem('侧向跳', studentEvaluation.student.e_shh, '次', studentEvaluation.p_shh))
    pr_items.append(PRItem('跳远', studentEvaluation.student.e_sws, '厘米', studentEvaluation.p_sws))
    pr_items.append(PRItem('20米冲刺跑', studentEvaluation.student.e_20m, '秒', studentEvaluation.p_20m))
    pr_items.append(PRItem('仰卧起坐', studentEvaluation.student.e_su, '重复次数', studentEvaluation.p_su))
    pr_items.append(PRItem('俯卧撑', studentEvaluation.student.e_ls, '重复次数', studentEvaluation.p_ls))
    pr_items.append(PRItem('直身前屈', studentEvaluation.student.e_rb, '厘米', studentEvaluation.p_rb))
    pr_items.append(PRItem('六分跑', studentEvaluation.student.e_lauf, '米', studentEvaluation.p_lauf))
    pr_items.append(PRItem('投掷', studentEvaluation.student.e_ball, '米', studentEvaluation.p_ball))
    
    return pr_items

class PRItem:
    def __init__(self, name, e_value, e_unit, p_value):
        self.name = name
        self.e_value = e_value
        self.e_unit = e_unit
        self.p_value = p_value

def getShanghaiMovementCheck2015StyleSheet():
    """Returns a stylesheet object"""
    stylesheet = StyleSheet1()

    stylesheet.add(ParagraphStyle(name='Normal',
                                  fontName='Microsoft-YaHei-Light',
                                  fontSize=9,
                                  leading=12)
                   )

    stylesheet.add(ParagraphStyle(name='Title',
                                  parent=stylesheet['Normal'],
                                  fontName='Microsoft-YaHei-Bold',
                                  fontSize=44,
                                  leading=66,
                                  alignment=TA_CENTER,
                                  spaceBefore=12,
                                  spaceAfter=3))

    stylesheet.add(ParagraphStyle(name='Subtitle',
                                  parent=stylesheet['Normal'],
                                  fontName='Microsoft-YaHei-Light',
                                  fontSize=16,
                                  leading=24,
                                  alignment=TA_CENTER,
                                  spaceAfter=3))
                   
    return stylesheet
        
class ShanghaiMovementCheck2015DocTemplate(BaseDocTemplate):
    styles  = getShanghaiMovementCheck2015StyleSheet()

    templateDir = os.path.join(os.path.dirname(__file__), '..'+os.sep+'storage'+os.sep+'CertificateTemplates'+os.sep+'ShanghaiMovementCheck2015')
    
    leftImageWidth, leftImageHeight = 2.82*cm, 14.84*cm
    leftImagePath = os.path.join(templateDir, 'Left.jpg')
    leftImage = Image(leftImagePath, width=leftImageWidth, height=leftImageHeight)
    leftImage.hAlign = 'LEFT'
    
    bottomImageWidth, bottomImageHeight = 18.75*cm, 2.13*cm
    bottomImagePath = os.path.join(templateDir, 'Bottom.jpg')
    bottomImage = Image(bottomImagePath, width=bottomImageWidth, height=bottomImageHeight)
    
    headerHeight = 5*cm
    footerHeight = 2.5*cm
    leftWidth = 4*cm
    signatureHeight = 2*cm

    def __init__(self, filename, **kw):
        kw['leftMargin'], kw['rightMargin'], kw['topMargin'], kw['bottomMargin'] = 1.27*cm, 1.27*cm, 1.27*cm, 1.27*cm
        BaseDocTemplate.__init__(self, filename, **kw)
    
    def afterNormalPage(self, canvas, doc):
        canvas.saveState()

        '''Footer Region'''
        w,h = self.pagesize[0], self.footerHeight
        x,y = 0, self.bottomMargin
        frameFooter = Frame(x, y, w, h, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
        frameFooter.addFromList([self.bottomImage], canvas)
        
        '''Left Region'''
        w,h = self.leftWidth, self.height - self.headerHeight - self.footerHeight
        x,y = self.leftMargin, self.pagesize[1] - self.topMargin - self.headerHeight - h
        frameLeft = Frame(x, y, w, h, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
        frameLeft.addFromList([self.leftImage], canvas)
        
        canvas.restoreState()
        
        return
        
    def build(self,flowables, canvasmaker=canvas.Canvas):
        """build the document using the flowables.  Annotate the first page using the onFirstPage
               function and later pages using the onLaterPages function.  The onXXX pages should follow
               the signature

                  def myOnFirstPage(canvas, document):
                      # do annotations and modify the document
                      ...

               The functions can do things like draw logos, page numbers,
               footers, etcetera. They can use external variables to vary
               the look (for example providing page numbering or section names).
        """
        self._calc()    #in case we changed margins sizes etc
        
        '''Header Region'''
        w,h = self.width, self.headerHeight
        x,y = self.leftMargin, self.pagesize[1] - self.topMargin - h
        frameHeader = Frame(x, y, w, h, id='Header')

        '''Content Region'''
        w,h = self.width - self.leftWidth, self.height - self.headerHeight - self.footerHeight - self.signatureHeight
        x,y = self.leftMargin + self.leftWidth, self.pagesize[1] - self.topMargin - self.headerHeight - h
        frameContent = Frame(x, y, w, h, id='Content')
        
        '''Signature Region'''
        w,h = w, self.signatureHeight
        x,y = x, y - h
        frameSignature = Frame(x, y, w, h, id='Signature')

        self.addPageTemplates([PageTemplate(id='Normal',frames=(frameHeader, frameContent, frameSignature), onPageEnd=self.afterNormalPage)])
        BaseDocTemplate.build(self,flowables, canvasmaker=canvasmaker) 
        
class PdfStudentBasicInfo(Flowable):
    def __init__(self, studentEvaluation, style):
        self.studentEvaluation = studentEvaluation
        self.style = style
    def wrap(self, availableWidth, availableHeight):
        height = 1.5*cm
        self.availableWidth = availableWidth
        self.height = height
        return (availableWidth, height)
    def draw(self):
        c = self.canv
        c.setFont(self.style.fontName, self.style.fontSize)
        student = self.studentEvaluation.student
        aW, aH = self.availableWidth, self.height
        header_w, data_w, h = 2*cm, self.availableWidth*0.5-2*cm, 0.5*cm
        c.drawString(self.availableWidth-aW,aH-h,'姓名:')
        aW = aW-header_w
        c.drawString(self.availableWidth-aW,aH-h,'%s%s' % (student.lastName, student.firstName))
        aW = aW-data_w
        c.drawString(self.availableWidth-aW,aH-h,'学校:')
        aW = aW-header_w
        c.drawString(self.availableWidth-aW,aH-h,str(student.schoolClass.school))
        aW, aH = self.availableWidth, aH-h
        c.drawString(self.availableWidth-aW,aH-h,'性别:')
        aW = aW-header_w
        c.drawString(self.availableWidth-aW,aH-h,student.get_gender_display())
        aW = aW-data_w
        c.drawString(self.availableWidth-aW,aH-h,'班级:')
        aW = aW-header_w
        c.drawString(self.availableWidth-aW,aH-h,str(student.schoolClass))

class PdfStudentComment(Flowable):
    def __init__(self, studentEvaluation, style):
        self.studentEvaluation = studentEvaluation
        self.style = style
    def wrap(self, availableWidth, availableHeight):
        height = 2.5*cm
        self.availableWidth = availableWidth
        self.height = height
        return (availableWidth, height)
    def draw(self):
        c = self.canv
        c.setFont(self.style.fontName, self.style.fontSize)
        studentEvaluation = self.studentEvaluation
        aW, aH = self.availableWidth, self.height
        data_w, h = self.availableWidth*0.5, 0.5*cm
        if studentEvaluation.is_frail:
            c.drawString(0,aH-h,'基于本次测试的综合表现，您的孩子需要进行运动健康干预。')
        else:
            c.drawString(0,aH-h,'基于本次测试的综合表现，您的孩子在以下这几个项目中具有较好的运动潜质：')
            aH = aH-h
            
            certificate_data = json.loads(studentEvaluation.certificate_data)
            potential_items = certificate_data['potential_items']
            potential_item_index = 0
            for potential_item in potential_items:
                potential_item_text = PdfStudentComment._get_potential_item_text(studentEvaluation, potential_item)
                c.drawString(self.availableWidth-aW,aH-h,potential_item_text)
                potential_item_index += 1
                if potential_item_index % 2 == 0:
                    aW, aH = self.availableWidth, aH-h
                else:
                    aW = aW-data_w
    def _get_potential_item_text(studentEvaluation, potential_item):
        if potential_item == 'badminton':
           potential_value = studentEvaluation.potential_badminton
           potential_name = '羽毛球(badminton)'
        elif potential_item == 'basketball':
           potential_value = studentEvaluation.potential_basketball
           potential_name = '篮球(basketball)'
        elif potential_item == 'soccer':
           potential_value = studentEvaluation.potential_soccer
           potential_name = '足球(soccer)'
        elif potential_item == 'gymnastics':
           potential_value = studentEvaluation.potential_gymnastics
           potential_name = '体操(gymnastics)'
        elif potential_item == 'canoe':
           potential_value = studentEvaluation.potential_canoe
           potential_name = '皮艇/划艇(canoe/kayak)'
        elif potential_item == 'discus':
           potential_value = studentEvaluation.potential_discus
           potential_name = '铁饼(discus)'
        elif potential_item == 'shot_put':
           potential_value = studentEvaluation.potential_shot_put
           potential_name = '铅球(shot put)'
        elif potential_item == 'pole_vault':
           potential_value = studentEvaluation.potential_pole_vault
           potential_name = '撑杆跳(pole vault)'
        elif potential_item == 'high_jump':
           potential_value = studentEvaluation.potential_high_jump
           potential_name = '跳高(high jump)'
        elif potential_item == 'javelin':
           potential_value = studentEvaluation.potential_javelin
           potential_name = '标枪(javelin)'
        elif potential_item == 'long_jump':
           potential_value = studentEvaluation.potential_long_jump
           potential_name = '跳远(long jump)'
        elif potential_item == 'huerdles':
           potential_value = studentEvaluation.potential_huerdles
           potential_name = '跨栏(huerdles)'
        elif potential_item == 'sprint':
           potential_value = studentEvaluation.potential_sprint
           potential_name = '短跑(sprint)'
        elif potential_item == 'rowing':
           potential_value = studentEvaluation.potential_rowing
           potential_name = '赛艇(rowing)'
        elif potential_item == 'swimming':
           potential_value = studentEvaluation.potential_swimming
           potential_name = '游泳(swimming)'
        elif potential_item == 'tennis':
           potential_value = studentEvaluation.potential_tennis
           potential_name = '网球(tennis)'
        elif potential_item == 'table_tennis':
           potential_value = studentEvaluation.potential_table_tennis
           potential_name = '乒乓球(table tennis)'
        elif potential_item == 'volleyball':
           potential_value = studentEvaluation.potential_volleyball
           potential_name = '排球(volleyball)'
        elif potential_item == 'athletics_running':
           potential_value = studentEvaluation.potential_athletics_running
           potential_name = '耐力跑(athletics - running)'
        elif potential_item == 'athletics_sprinting_jumping_throwing':
           potential_value = studentEvaluation.potential_athletics_sprinting_jumping_throwing
           potential_name = '跑跳投(athletics - sprinting/jumping/throwing)'
        return '%s %s' % ("{0:.0%}".format(potential_value), potential_name)