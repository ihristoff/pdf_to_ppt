import os
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
from pdf_to_ppt import convert_pdf_to_ppt
import uuid

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        pdf_filename = secure_filename(f"{unique_id}.pdf")
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
        
        # Save uploaded file
        file.save(pdf_path)
        
        try:
            # Convert PDF to PPT
            ppt_filename = f"{unique_id}.pptx"
            ppt_path = os.path.join(app.config['UPLOAD_FOLDER'], ppt_filename)
            convert_pdf_to_ppt(pdf_path, ppt_path)
            
            # Clean up PDF file
            os.remove(pdf_path)
            
            return jsonify({
                'success': True,
                'filename': ppt_filename,
                'message': 'File converted successfully!'
            })
            
        except Exception as e:
            # Clean up files in case of error
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            if os.path.exists(ppt_path):
                os.remove(ppt_path)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True) 