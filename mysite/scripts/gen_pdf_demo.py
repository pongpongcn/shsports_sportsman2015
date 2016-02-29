from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics, ttfonts

def run():
    #pdfmetrics.registerFont(ttfonts.TTFont("simsun", "simsun.ttc"))

    canvas = Canvas("test.pdf")

    for font in canvas.getAvailableFonts():
        print(font)

    #canvas.setFont('simsun', 32)
    canvas.drawString(10, 150, 'Some text')

    canvas.save()
    print('Done!')
