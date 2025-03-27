from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Line, Circle, Rect, Polygon, String
from reportlab.graphics import renderPDF
import math

def create_test_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    styles = getSampleStyleSheet()
    
    # Page 1: Text Styles and Basic Shapes
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, "Test Page 1: Text and Basic Shapes")
    
    # Different text styles
    y = height - 150
    c.setFont("Helvetica", 12)
    c.drawString(100, y, "Regular text")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y - 20, "Bold text")
    
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(100, y - 40, "Italic text")
    
    c.setFont("Helvetica-BoldOblique", 12)
    c.drawString(100, y - 60, "Bold Italic text")
    
    # Bullet points with different levels
    y = y - 100
    c.setFont("Helvetica", 12)
    c.drawString(100, y, "• First level bullet")
    c.drawString(120, y - 20, "○ Second level bullet")
    c.drawString(140, y - 40, "▪ Third level bullet")
    
    # Basic shapes with different colors
    # Rectangle
    c.setFillColorRGB(1, 0, 0)  # Red
    c.setStrokeColorRGB(0, 0, 0)  # Black border
    c.rect(100, y - 100, 100, 50, fill=1)
    
    # Circle
    c.setFillColorRGB(0, 0, 1)  # Blue
    c.circle(300, y - 75, 25, fill=1)
    
    # Triangle
    c.setFillColorRGB(0, 1, 0)  # Green
    p = c.beginPath()
    p.moveTo(400, y - 100)
    p.lineTo(450, y - 100)
    p.lineTo(425, y - 50)
    p.close()
    c.drawPath(p, fill=1)
    
    c.showPage()
    
    # Page 2: Complex Shapes and Gradients
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, "Test Page 2: Complex Shapes")
    
    # Create a star
    y = height - 200
    points = 5
    outer_radius = 50
    inner_radius = 20
    center_x = 150
    center_y = y
    
    p = c.beginPath()
    angle = math.pi / points
    
    # First point
    p.moveTo(center_x + outer_radius * math.cos(0),
             center_y + outer_radius * math.sin(0))
    
    # Draw the star
    for i in range(1, 2 * points + 1):
        radius = outer_radius if i % 2 == 0 else inner_radius
        x = center_x + radius * math.cos(i * angle)
        y = center_y + radius * math.sin(i * angle)
        p.lineTo(x, y)
    
    p.close()
    c.setFillColorRGB(1, 1, 0)  # Yellow
    c.setStrokeColorRGB(1, 0.5, 0)  # Orange border
    c.drawPath(p, fill=1, stroke=1)
    
    # Gradient rectangle
    y = y - 100
    for i in range(100):
        c.setStrokeColorRGB(i/100, 0, 1-i/100)
        c.line(100, y+i, 300, y+i)
    
    # Dashed lines
    y = y - 50
    c.setDash([5, 10])
    c.setStrokeColorRGB(0, 0, 0)
    c.line(100, y, 300, y)
    
    c.setDash([10, 5])
    c.line(100, y - 20, 300, y - 20)
    
    c.setDash([15, 5, 5, 5])
    c.line(100, y - 40, 300, y - 40)
    
    c.showPage()
    
    # Page 3: Text Layouts and Tables
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, "Test Page 3: Layout Elements")
    
    # Create a simple table
    y = height - 200
    table_data = [
        ["Header 1", "Header 2", "Header 3"],
        ["Cell 1,1", "Cell 1,2", "Cell 1,3"],
        ["Cell 2,1", "Cell 2,2", "Cell 2,3"]
    ]
    
    cell_width = 100
    cell_height = 30
    
    for row_idx, row in enumerate(table_data):
        for col_idx, cell in enumerate(row):
            x = 100 + col_idx * cell_width
            current_y = y - row_idx * cell_height
            
            # Draw cell borders
            c.rect(x, current_y - cell_height, cell_width, cell_height)
            
            # Draw cell text
            c.setFont("Helvetica", 12)
            if row_idx == 0:  # Header row
                c.setFont("Helvetica-Bold", 12)
            c.drawString(x + 5, current_y - 20, cell)
    
    # Two-column text layout
    y = y - 150
    col_width = 200
    c.setFont("Helvetica", 10)
    
    left_text = "This is the left column of text. It demonstrates multi-column layout capabilities."
    right_text = "This is the right column of text. It shows how content can be arranged in columns."
    
    c.drawString(100, y, left_text)
    c.drawString(350, y, right_text)
    
    # Add some decorative elements
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.line(320, y + 30, 320, y - 50)  # Vertical separator
    
    c.save()
    print("Test PDF created successfully!")

if __name__ == "__main__":
    create_test_pdf("test.pdf") 