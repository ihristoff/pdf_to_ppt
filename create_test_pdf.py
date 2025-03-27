from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_test_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    styles = getSampleStyleSheet()
    
    # Page 1
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, "Test Page 1")
    
    c.setFont("Helvetica", 16)
    c.drawString(100, height - 150, "This is a test document for PDF to PowerPoint conversion")
    c.drawString(100, height - 200, "Testing text rendering and layout")
    
    # Draw some shapes
    c.setStrokeColor(colors.blue)
    c.rect(100, height - 300, 200, 50, fill=0)
    c.setFillColor(colors.red)
    c.circle(400, height - 275, 25, fill=1)
    
    c.showPage()
    
    # Page 2
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, "Test Page 2")
    
    c.setFont("Helvetica", 16)
    bullet_points = [
        "Multiple page conversion",
        "Text rendering",
        "Shape preservation",
        "Color accuracy"
    ]
    
    for i, point in enumerate(bullet_points):
        c.drawString(120, height - 150 - (i * 30), f"• {point}")
    
    c.showPage()
    
    # Page 3
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, "Test Page 3")
    
    c.setFont("Helvetica", 16)
    c.drawString(100, height - 150, "Final test page")
    c.drawString(100, height - 200, "If you can read this, the conversion was successful!")
    
    # Draw a gradient rectangle
    for i in range(100):
        c.setStrokeColor(colors.Color(i/100, 0, 1-i/100))
        c.line(100, height-300+i, 500, height-300+i)
    
    c.save()

if __name__ == "__main__":
    create_test_pdf("test.pdf")
    print("Test PDF created successfully!") 