from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, BaseDocTemplate, Frame, PageBreak, PageTemplate, Table, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import cm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable
import os, json
from io import BytesIO
from reportlab.lib import colors
from decimal import Decimal

class CertificateGenerator:
    def gen_certificate(studentEvaluations):
        pdfmetrics.registerFont(TTFont("simsun", "simsun.ttc"))
        
        buffer = BytesIO()

        doc = ShanghaiMovementCheck2015DocTemplate(buffer)
        Story = []
        styles = {
            'Normal': ParagraphStyle('Normal', fontName='simsun', fontSize=9, leading=11),
            'BodyText': ParagraphStyle('Normal', fontName='simsun', fontSize=9, leading=11, spaceBefore=6),
        }
        
        for studentEvaluation in studentEvaluations:
            pdfStudentBasicInfo = PdfStudentBasicInfo(studentEvaluation, style=styles['Normal'])
            Story.append(pdfStudentBasicInfo)
            
            p = Paragraph('您在2015年上海运动能力测试中的表现', styles['BodyText'])
            Story.append(p)
            
            pdfStudentPRChart = PdfStudentPRChart(studentEvaluation, style=styles['Normal'])
            Story.append(pdfStudentPRChart)
            
            p = Paragraph('50%表示同年龄段孩子所具备运动能力的平均水平,百分比值越高代表孩子具备的运动能力越突出。百分比只 是运动能力的参考值。', styles['BodyText'])
            Story.append(p)
            
            Story.append(Spacer(0, 2*cm))
            
            p = Paragraph('尊敬的家长： 感谢您的孩子参加了我们的运动能力测试！ 您的孩子正处于各项身体素质发展的关键敏感期。这个阶段也是传统意义上的儿童体育运动阶段。让孩子参 加到各种儿童体育运动中去,将为孩子运动机能的全面发展提供重要的机会。跳、跑、踢、抛、接、滑动、转 动等能力,如果得到综合的运用和锻炼,将使孩子的手、眼、脑、四肢、肌肉、神经、心理得到均衡发展,并使 您的孩子茁壮成长。', styles['BodyText'])
            Story.append(p)
            
            pdfStudentComment = PdfStudentComment(studentEvaluation, style=styles['Normal'])
            Story.append(pdfStudentComment)

            Story.append(Spacer(0, 3.5*cm))
            
            p = Paragraph('''上海市青少年体育选材育才中心 Shanghai Sports Talent Identification & Development Center
德国拜罗伊特大学 University of Bayreuth - Training & Movement Science''', styles['Normal'])
            Story.append(p)
            
            Story.append(PageBreak())

        doc.build(Story)

        pdf = buffer.getvalue()
        buffer.close()
        
        return pdf
        
class ShanghaiMovementCheck2015DocTemplate(BaseDocTemplate):
    styles = {
            'Title': ParagraphStyle('Title', fontName='simsun', fontSize=44, leading=66, alignment=TA_CENTER),
            'SubTitle': ParagraphStyle('SubTitle', fontName='simsun', fontSize=16, leading=24, alignment=TA_CENTER)
        }

    templateImageLeftPath_width, templateImageLeftPath_height = 2.82*cm, 13.19*cm
    templateImageLeftPath = os.path.join(os.path.dirname(__file__), '../storage/CertificateTemplates/ShanghaiMovementCheck2015/Left.jpg')
    templateImageLeft = Image(templateImageLeftPath, width=templateImageLeftPath_width, height=templateImageLeftPath_height)
    
    templateImageBottom_width, templateImageBottom_height = 18.75*cm, 2.13*cm
    templateImageBottomPath = os.path.join(os.path.dirname(__file__), '../storage/CertificateTemplates/ShanghaiMovementCheck2015/Bottom.jpg')
    templateImageBottom = Image(templateImageBottomPath, width=templateImageBottom_width, height=templateImageBottom_height)
        
    def normalPages(self, canvas, doc):
        canvas.saveState()

        aW = doc.pagesize[0] # available width and height
        aH = doc.pagesize[1]
        
        p_title = Paragraph('证书', self.styles['Title'])
        w,h = p_title.wrap(aW, aH) # find required space
        p_title.drawOn(canvas,0,aH-h)
        aH = aH - h
        
        p_sub_title = Paragraph('2015年上海运动能力测试 - Shanghai Movement Check 2015', self.styles['SubTitle'])
        w,h = p_sub_title.wrap(aW, aH) # find required space
        p_sub_title.drawOn(canvas,0,aH-h)
        aH = aH - h
        
        self.templateImageLeft.drawOn(canvas, 0.8*cm, aH-self.templateImageLeftPath_height-1*cm)
        self.templateImageBottom.drawOn(canvas, (aW-self.templateImageBottom_width)/2, 1*cm)
        
        canvas.restoreState()
        
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
        frameT_leftMargin, frameT_bottomMargin, frameT_topMargin, frameT_rightMargin = 3.8*cm, 4*cm, 4*cm, 0.8*cm
        frameT = Frame(frameT_leftMargin, frameT_bottomMargin, self.width+self.leftMargin+self.rightMargin-frameT_leftMargin-frameT_rightMargin, self.height+self.bottomMargin+self.topMargin-frameT_bottomMargin-frameT_topMargin)
        self.addPageTemplates([PageTemplate(id='Normal',frames=frameT, onPage=self.normalPages,pagesize=self.pagesize)])
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
        c.drawString(self.availableWidth-aW,aH-h,'姓:')
        aW = aW-header_w
        c.drawString(self.availableWidth-aW,aH-h,student.lastName)
        aW = aW-data_w
        c.drawString(self.availableWidth-aW,aH-h,'学校:')
        aW = aW-header_w
        c.drawString(self.availableWidth-aW,aH-h,str(student.schoolClass.school))
        aW, aH = self.availableWidth, aH-h
        c.drawString(self.availableWidth-aW,aH-h,'名:')
        aW = aW-header_w
        c.drawString(self.availableWidth-aW,aH-h,student.firstName)
        aW = aW-data_w
        c.drawString(self.availableWidth-aW,aH-h,'班级:')
        aW = aW-header_w
        c.drawString(self.availableWidth-aW,aH-h,str(student.schoolClass))

class PdfStudentPRChart(Flowable):
    imagePRChartSkeleton_width, imagePRChartSkeleton_height = 14.12*cm, 6.35*cm
    imagePRChartSkeletonPath = os.path.join(os.path.dirname(__file__), '../storage/CertificateTemplates/ShanghaiMovementCheck2015/PRChartSkeleton.jpg')
    imagePRChartSkeleton = Image(imagePRChartSkeletonPath, width=imagePRChartSkeleton_width, height=imagePRChartSkeleton_height)
    
    def __init__(self, studentEvaluation, style):
        self.studentEvaluation = studentEvaluation
        self.style = style
    def wrap(self, availableWidth, availableHeight):
        height = self.imagePRChartSkeleton_height
        self.height = height
        return (availableWidth, height)
    def draw(self):
        c = self.canv
        c.setFont(self.style.fontName, self.style.fontSize)
        self.imagePRChartSkeleton.drawOn(c, 0, 0)
        
        scoreItem_offset_x = 1.5*cm
        lineHeight = 0.587*cm
        stripHeight = 0.4*cm
        stripWidth = 12.4*cm
        
        aH = self.height - 0.85*cm

        for item in PdfStudentPRChart._get_pr_items(self.studentEvaluation):
            percentage = item.p_value * 0.01
            c.saveState()
            c.setFillColor(colors.HexColor('#7fd8ff'))
            c.rect(scoreItem_offset_x,aH-stripHeight,Decimal(stripWidth)*Decimal(percentage),stripHeight, fill=1, stroke=0)
            c.restoreState()
            
            pr_text = '%s%%(%s %s)' % (item.p_value, item.e_value, item.e_unit)
            c.drawString(scoreItem_offset_x,aH-stripHeight+0.09*cm,pr_text)
            
            aH -= lineHeight

    def _get_pr_items(studentEvaluation):
        pr_items = []
        pr_items.append(PdfStudentPRChart.PRItem('平衡', studentEvaluation.student.e_bal, '步', studentEvaluation.p_bal))
        pr_items.append(PdfStudentPRChart.PRItem('侧向跳', studentEvaluation.student.e_shh, '次', studentEvaluation.p_shh))
        pr_items.append(PdfStudentPRChart.PRItem('跳远', studentEvaluation.student.e_sws, '厘米', studentEvaluation.p_sws))
        pr_items.append(PdfStudentPRChart.PRItem('20米冲刺跑', studentEvaluation.student.e_20m, '秒', studentEvaluation.p_20m))
        pr_items.append(PdfStudentPRChart.PRItem('仰卧起坐', studentEvaluation.student.e_su, '重复次数', studentEvaluation.p_su))
        pr_items.append(PdfStudentPRChart.PRItem('俯卧撑', studentEvaluation.student.e_ls, '重复次数', studentEvaluation.p_ls))
        pr_items.append(PdfStudentPRChart.PRItem('直身前屈', studentEvaluation.student.e_rb, '厘米', studentEvaluation.p_rb))
        pr_items.append(PdfStudentPRChart.PRItem('六分跑', studentEvaluation.student.e_lauf, '米', studentEvaluation.p_lauf))
        pr_items.append(PdfStudentPRChart.PRItem('投掷', studentEvaluation.student.e_ball, '米', studentEvaluation.p_ball))
        
        return pr_items

    class PRItem:
        def __init__(self, name, e_value, e_unit, p_value):
            self.name = name
            self.e_value = e_value
            self.e_unit = e_unit
            self.p_value = p_value
    
class PdfStudentComment(Flowable):
    def __init__(self, studentEvaluation, style):
        self.studentEvaluation = studentEvaluation
        self.style = style
    def wrap(self, availableWidth, availableHeight):
        height = 3*cm
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
            c.drawString(0,aH-h,'基于本次测试的综合表现,您的孩子需要进行运动健康干预。')
        else:
            c.drawString(0,aH-h,'基于本次测试的综合表现,您的孩子在以下这几个项目中具有较好的运动潜质：')
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