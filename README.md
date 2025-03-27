# PDF to PowerPoint Converter

This tool converts PDF files to PowerPoint presentations by creating a slide for each page in the PDF.

## Prerequisites

- Python 3.6 or higher
- Poppler (required for pdf2image)

### Installing Poppler

#### Windows
1. Download Poppler from: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract the downloaded file
3. Add the `bin` directory to your system's PATH environment variable

#### Linux
```bash
sudo apt-get install poppler-utils
```

#### macOS
```bash
brew install poppler
```

## Installation

1. Clone this repository or download the files
2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python pdf_to_ppt.py input.pdf
```

Specify custom output path:
```bash
python pdf_to_ppt.py input.pdf -o output.pptx
```

## Features

- Converts each PDF page to a separate PowerPoint slide
- Maintains aspect ratio of the original content
- Automatically centers content on slides
- Supports custom output file paths
- Progress tracking during conversion

## Notes

- The quality of the conversion depends on the quality of the input PDF
- Text in the PDF will be converted to images, so it won't be editable in PowerPoint
- Large PDF files may take longer to process 