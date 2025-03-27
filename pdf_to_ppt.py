import os
from pdf2image import convert_from_path
from pptx import Presentation
from pptx.util import Inches
from PIL import Image
import argparse
import sys

def convert_pdf_to_ppt(pdf_path, output_path=None):
    """
    Convert a PDF file to a PowerPoint presentation.
    
    Args:
        pdf_path (str): Path to the input PDF file
        output_path (str, optional): Path for the output PowerPoint file. 
                                   If not provided, will use the same name as PDF with .pptx extension
    """
    try:
        # If no output path is specified, create one based on the input file
        if output_path is None:
            output_path = os.path.splitext(pdf_path)[0] + '.pptx'
        
        # Create a new PowerPoint presentation
        prs = Presentation()
        
        # Convert PDF pages to images
        print(f"Converting PDF pages to images...")
        
        # Use local Poppler installation
        poppler_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poppler", "poppler-24.08.0", "Library", "bin")
        
        if not os.path.exists(poppler_path):
            raise Exception(
                "Poppler not found in the expected location. "
                "Please ensure Poppler is properly installed in the 'poppler' directory."
            )
        
        images = convert_from_path(pdf_path, poppler_path=poppler_path)
        
        if not images:
            raise Exception("No pages found in the PDF file")
        
        # Add each image as a new slide
        for i, image in enumerate(images):
            print(f"Processing page {i+1}/{len(images)}...")
            
            # Add a new slide with title and content layout
            slide = prs.slides.add_slide(prs.slide_layouts[5])
            
            # Get the slide dimensions
            slide_width = prs.slide_width
            slide_height = prs.slide_height
            
            # Calculate image dimensions to fit the slide while maintaining aspect ratio
            img_width, img_height = image.size
            aspect_ratio = img_width / img_height
            
            if aspect_ratio > 1:
                # Image is wider than tall
                new_width = slide_width
                new_height = int(slide_width / aspect_ratio)
                left = 0
                top = (slide_height - new_height) // 2
            else:
                # Image is taller than wide
                new_height = slide_height
                new_width = int(slide_height * aspect_ratio)
                left = (slide_width - new_width) // 2
                top = 0
            
            # Save image to temporary file (required for add_picture)
            temp_img_path = f"temp_slide_{i}.png"
            image.save(temp_img_path, "PNG")
            
            try:
                # Add the image to the slide
                slide.shapes.add_picture(temp_img_path, left, top, width=new_width, height=new_height)
            finally:
                # Clean up temporary file
                if os.path.exists(temp_img_path):
                    os.remove(temp_img_path)
        
        # Save the presentation
        print(f"Saving PowerPoint presentation to {output_path}...")
        prs.save(output_path)
        print("Conversion completed successfully!")
        
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        raise Exception(f"Failed to convert PDF: {str(e)}")

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