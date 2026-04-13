import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from document_processor import DocumentProcessor
import markdown

# Load environment variables
load_dotenv()

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'md'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB limit

# Initialize App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = os.getenv('SECRET_KEY', 'supersecretkey_change_this_in_production')

# Initialize Processor
processor = DocumentProcessor(UPLOAD_FOLDER)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.template_filter('markdown')
def render_markdown(text):
    return markdown.markdown(text, extensions=['fenced_code', 'tables'])

@app.route('/')
def index():
    files = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            metadata = processor.get_file_metadata(filename)
            if metadata:
                files.append(metadata)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        logger.info(f"File uploaded: {filename}")
        flash('File successfully uploaded')
        return redirect(url_for('view_document', filename=filename))
    else:
        flash('Allowed file types are txt, pdf, docx, md')
        return redirect(request.url)

@app.route('/view/<filename>')
def view_document(filename):
    safe_filename = secure_filename(filename)
    metadata = processor.get_file_metadata(safe_filename)
    
    if not metadata:
        abort(404)
        
    result = processor.process_document(safe_filename)
    
    if not result['success']:
        flash(f"Error processing file: {result.get('error')}")
        return redirect(url_for('index'))
        
    return render_template('view.html', metadata=metadata, content=result['content'])

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    safe_filename = secure_filename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
    
    if os.path.exists(filepath):
        os.remove(filepath)
        flash('File deleted successfully')
    else:
        flash('File not found')
        
    return redirect(url_for('index'))

@app.errorhandler(413)
def request_entity_too_large(error):
    flash('File too large. Limit is 10MB.')
    return redirect(url_for('index')), 413

if __name__ == '__main__':
    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, port=5000)
