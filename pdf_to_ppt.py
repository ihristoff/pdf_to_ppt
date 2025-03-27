import os
import fitz  # PyMuPDF
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import re
import argparse
import sys

def hex_to_rgb(hex_color):
    """Convert hex color to RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def is_bullet_character(text):
    """Check if the text starts with a bullet point character."""
    bullet_chars = ['•', '·', '○', '●', '▪', '▫', '◦', '-', '*']
    return any(text.strip().startswith(char) for char in bullet_chars)

def clean_bullet_text(text):
    """Remove bullet character from the beginning of text."""
    bullet_chars = ['•', '·', '○', '●', '▪', '▫', '◦', '-', '*']
    text = text.strip()
    for char in bullet_chars:
        if text.startswith(char):
            return text[len(char):].strip()
    return text

def convert_pdf_to_ppt(pdf_path, output_path=None):
    """
    Convert a PDF file to a PowerPoint presentation with editable elements.
    
    Args:
        pdf_path (str): Path to the input PDF file
        output_path (str, optional): Path for the output PowerPoint file. 
                                   If not provided, will use the same name as PDF with .pptx extension
    """
    try:
        if output_path is None:
            output_path = os.path.splitext(pdf_path)[0] + '.pptx'
        
        # Create presentation with 16:9 aspect ratio
        prs = Presentation()
        prs.slide_width = Inches(16)
        prs.slide_height = Inches(9)
        
        pdf_document = fitz.open(pdf_path)
        print(f"Converting PDF with {len(pdf_document)} pages...")
        
        for page_num in range(len(pdf_document)):
            print(f"Processing page {page_num + 1}/{len(pdf_document)}...")
            
            page = pdf_document[page_num]
            # Use blank layout for more control
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            
            # Get page dimensions
            pdf_width = page.rect.width
            pdf_height = page.rect.height
            
            # Scale factor for converting PDF points to PowerPoint inches
            scale_x = prs.slide_width / pdf_width
            scale_y = prs.slide_height / pdf_height
            
            # Extract text blocks with formatting
            text_blocks = page.get_text("dict")["blocks"]
            
            for block in text_blocks:
                if "lines" not in block:
                    continue
                
                # Get the block's bounding box
                bbox = block["bbox"]
                x0, y0, x1, y1 = bbox
                
                # Convert PDF coordinates to PowerPoint coordinates
                left = x0 * scale_x
                top = y0 * scale_y
                width = (x1 - x0) * scale_x
                height = (y1 - y0) * scale_y
                
                # Create text box
                text_box = slide.shapes.add_textbox(
                    left, top, width, height
                )
                
                text_frame = text_box.text_frame
                text_frame.word_wrap = True
                text_frame.auto_size = MSO_ANCHOR.TOP
                
                # Process each line in the block
                for line in block["lines"]:
                    # Create a new paragraph for each line
                    if text_frame.paragraphs:
                        paragraph = text_frame.add_paragraph()
                    else:
                        paragraph = text_frame.paragraphs[0]
                    
                    # Check if this line starts with a bullet point
                    first_span = line["spans"][0] if line["spans"] else None
                    is_bullet = first_span and is_bullet_character(first_span["text"])
                    
                    if is_bullet:
                        paragraph.level = 0
                        # Enable bullets for this paragraph
                        paragraph.style = 'List Paragraph'
                    
                    # Process spans in the line
                    for span in line["spans"]:
                        text = span["text"]
                        if is_bullet and span == first_span:
                            text = clean_bullet_text(text)
                        
                        run = paragraph.add_run()
                        run.text = text
                        
                        # Set font properties
                        font = run.font
                        font.name = span.get("font", "Calibri")
                        font.size = Pt(span["size"])
                        
                        # Handle font styles
                        flags = span.get("flags", 0)
                        font.bold = bool(flags & 2**4)  # Check if bold flag is set
                        font.italic = bool(flags & 2**1)  # Check if italic flag is set
                        
                        # Handle colors
                        if "color" in span:
                            color = span["color"]
                            if isinstance(color, list) and len(color) >= 3:
                                r, g, b = [int(c * 255) for c in color[:3]]
                                font.color.rgb = RGBColor(r, g, b)
            
            # Extract and convert shapes
            for shape in page.get_drawings():
                # Get shape coordinates
                rect = shape["rect"]
                x0, y0, x1, y1 = rect
                left = x0 * scale_x
                top = y0 * scale_y
                width = (x1 - x0) * scale_x
                height = (y1 - y0) * scale_y
                
                # Create a basic shape (rectangle as fallback)
                ppt_shape = slide.shapes.add_shape(
                    MSO_SHAPE.RECTANGLE, left, top, width, height
                )
                
                # Try to determine fill color from the shape items
                if shape.get("fill"):
                    fill = shape["fill"]
                    if isinstance(fill, list) and len(fill) >= 3:
                        r, g, b = [int(c * 255) for c in fill[:3]]
                        ppt_shape.fill.solid()
                        ppt_shape.fill.fore_color.rgb = RGBColor(r, g, b)
                
                # Try to determine stroke color from the shape items
                if shape.get("stroke"):
                    stroke = shape["stroke"]
                    if isinstance(stroke, list) and len(stroke) >= 3:
                        r, g, b = [int(c * 255) for c in stroke[:3]]
                        ppt_shape.line.color.rgb = RGBColor(r, g, b)
        
        print(f"Saving PowerPoint presentation to {output_path}...")
        prs.save(output_path)
        print("Conversion completed successfully!")
        
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        raise Exception(f"Failed to convert PDF: {str(e)}")
    finally:
        if 'pdf_document' in locals():
            pdf_document.close()

def main():
    parser = argparse.ArgumentParser(description='Convert PDF file to PowerPoint presentation')
    parser.add_argument('pdf_path', help='Path to the input PDF file')
    parser.add_argument('--output', '-o', help='Path for the output PowerPoint file (optional)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_path):
        print(f"Error: The file {args.pdf_path} does not exist.")
        return
    
    try:
        convert_pdf_to_ppt(args.pdf_path, args.output)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 