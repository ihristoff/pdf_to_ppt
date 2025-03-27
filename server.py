from flask import Flask, request, send_file
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from pdf_to_ppt import convert_pdf_to_ppt
import tempfile

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    
    if file and allowed_file(file.filename):
        try:
            # Create temporary files for input and output
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_temp:
                file.save(pdf_temp.name)
                
            with tempfile.NamedTemporaryFile(suffix='.pptx', delete=False) as pptx_temp:
                # Convert PDF to PPTX
                convert_pdf_to_ppt(pdf_temp.name, pptx_temp.name)
                
                # Send the converted file
                return send_file(
                    pptx_temp.name,
                    as_attachment=True,
                    download_name='converted.pptx',
                    mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
                )
        
        except Exception as e:
            return {'error': str(e)}, 500
        
        finally:
            # Clean up temporary files
            try:
                os.unlink(pdf_temp.name)
                os.unlink(pptx_temp.name)
            except:
                pass
    
    return {'error': 'Invalid file type'}, 400

if __name__ == '__main__':
    app.run(debug=True, port=5000) 