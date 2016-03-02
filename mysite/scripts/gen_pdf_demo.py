import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def run():
    pdfmetrics.registerFont(TTFont('Microsoft YaHei', 'msyh.ttc'))
    pdfmetrics.registerFont(TTFont('Microsoft YaHei Bold', 'msyhbd.ttc'))
    pdfmetrics.registerFont(TTFont('Microsoft YaHei Light', 'msyhl.ttc'))
    pdfmetrics.registerFontFamily('Microsoft YaHei',normal='Microsoft YaHei',bold='Microsoft YaHei Bold')

    styles = getSampleStyleSheet()
    
    story = []

    story.append(Paragraph('''<font name="Microsoft YaHei"><b>粗体</b></font>''', styles['Normal']))
    story.append(Paragraph('''<font name="Microsoft YaHei Bold">粗体</font>''', styles['Normal']))
    story.append(Paragraph('''<font name="Times-Roman"><b>Bold</b></font>''', styles['Normal']))
    story.append(Paragraph('''<font name="times"><b>Bold</b></font>''', styles['Normal']))
    story.append(Paragraph('''<font name="Courier"><b>Bold</b></font>''', styles['Normal']))
    story.append(Paragraph('''<font name="courier"><b>Bold</b></font>''', styles['Normal']))
    
    
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
    pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))
    pdfmetrics.registerFontFamily('Vera',normal='Vera',bold='VeraBd',italic='VeraIt',boldItalic='VeraBI')
    
    styleN = styles['Normal']
    styleH = styles['Heading1']

    
    #add some flowables
    story.append(Paragraph("This is a Heading",styleH))
    story.append(Paragraph("This is a paragraph in <i>Normal</i> style.", styleN))
    story.append(Paragraph('''<font name="Times-Roman"
size="14">This is in
Times-Roman</font> <font
name="Vera" color="magenta"
size="14">and this is in magenta
<b>Vera!</b></font>''', styleN))

    c = Canvas('test.pdf')
    f = Frame(inch, inch, 6*inch, 9*inch, showBoundary=1)
    f.addFromList(story,c)
    c.save()
    
    print('Done!')
