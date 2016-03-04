from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Image
from reportlab.pdfgen import canvas
import os

pdfmetrics.registerFont(TTFont("SimSun", "simsun.ttc"))

class StudentDataFormGenerator:
    def __init__(self, filename):
        self.filename = filename
    
    def build(self, students):  
        pagesize = landscape(A4)
        fontName = 'SimSun'

        templateImagePath = os.path.join(os.path.dirname(__file__), '..'+os.sep+'resources'+os.sep+'DataSheetTemplate.jpg')
        templateImage = Image(templateImagePath, width=29.7*cm, height=21*cm)

        p = canvas.Canvas(self.filename, pagesize=pagesize)
        for student in students:
            templateImage.drawOn(p, 0, 0)
            p.setFont(fontName, 12)
            p.drawString(4.4*cm, pagesize[1]-2.93*cm, '%s, %s' % (student.lastName, student.firstName))
            p.drawString(11.9*cm, pagesize[1]-2.93*cm, str(student.number))
            if student.gender:
                p.drawString(3.9*cm, pagesize[1]-3.63*cm, student.get_gender_display())
            p.drawString(11.9*cm, pagesize[1]-3.63*cm, str(student.dateOfBirth))
            p.drawString(3.9*cm, pagesize[1]-4.35*cm, student.schoolClass.school.name)
            p.drawString(11.1*cm, pagesize[1]-4.35*cm, str(student.schoolClass))
            p.drawString(4.8*cm, pagesize[1]-5.02*cm, str(student.dateOfTesting))
            p.showPage()
            
        p.save()