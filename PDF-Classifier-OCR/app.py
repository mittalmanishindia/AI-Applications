import os
import shutil
import json
import time
import logging
import datetime
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Library imports with error handling
try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None
    Image = None

try:
    import docx
except ImportError:
    docx = None

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, 'input_documents')
PROJECT_ROOT = os.path.join(BASE_DIR, 'project_root')
CLASSES_DIR = os.path.join(PROJECT_ROOT, 'classes')
EXTRACTED_DIR = os.path.join(PROJECT_ROOT, 'extracted')
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'activity.log')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Setup Flask
app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# Setup Gemini LLM
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None
    logging.warning("GEMINI_API_KEY not found. LLM classification will be disabled.")

def setup_directories():
    """Creates the necessary directory structure."""
    dirs = [INPUT_DIR, PROJECT_ROOT, CLASSES_DIR, EXTRACTED_DIR, LOG_DIR, TEMPLATE_DIR]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    # Setup Logging
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def extract_text_from_pdf(filepath):
    text = ""
    if pdfplumber:
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            logging.error(f"Error reading PDF {filepath}: {e}")
    
    if not text.strip() and pytesseract and Image:
        try:
            # Placeholder for OCR logic if needed
            pass 
        except Exception:
            pass
    return text

def extract_text_from_docx(filepath):
    text = ""
    if docx:
        try:
            doc = docx.Document(filepath)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            logging.error(f"Error reading DOCX {filepath}: {e}")
    return text

def extract_text_from_image(filepath):
    text = ""
    if pytesseract and Image:
        try:
            with Image.open(filepath) as img:
                text = pytesseract.image_to_string(img)
        except Exception as e:
            logging.error(f"Error OCRing image {filepath}: {e}")
    return text

def extract_text_from_txt(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error reading TXT {filepath}: {e}")
        return ""

def classify_with_llm(text, filename):
    """Classifies document using Gemini LLM."""
    if not model:
        return "Uncertain (No LLM)"
    
    prompt = f"""
    You are an intelligent document classifier. 
    Analyze the following text extracted from a document named "{filename}".
    
    Classify it into ONE of these categories:
    - Invoice
    - Contract
    - Report
    - Form
    - Technical
    - Resume
    - Other

    Return ONLY the category name.

    Document Text (truncated):
    {text[:2000]}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logging.error(f"LLM Error: {e}")
        return "Uncertain (LLM Error)"

def process_file(filepath, filename):
    """Main processing logic."""
    logging.info(f"Processing {filename}...")
    
    # 1. Extract
    ext = os.path.splitext(filename)[1].lower()
    content = ""
    
    if ext == '.pdf':
        content = extract_text_from_pdf(filepath)
    elif ext == '.docx':
        content = extract_text_from_docx(filepath)
    elif ext in ['.jpg', '.jpeg', '.png', '.tiff']:
        content = extract_text_from_image(filepath)
    elif ext == '.txt':
        content = extract_text_from_txt(filepath)
    else:
        return "Unsupported File Type"

    # 2. Classify (LLM)
    category = classify_with_llm(content, filename)
    logging.info(f"Classified {filename} as {category}")

    # 3. Move File
    dest_folder = os.path.join(CLASSES_DIR, category)
    os.makedirs(dest_folder, exist_ok=True)
    dest_path = os.path.join(dest_folder, filename)
    
    # Handle duplicate filenames in destination
    if os.path.exists(dest_path):
        base, extension = os.path.splitext(filename)
        timestamp = int(time.time())
        dest_path = os.path.join(dest_folder, f"{base}_{timestamp}{extension}")
    
    # Retry logic for moving file (handles Windows file locking)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            logging.info(f"Attempting to move {filepath} to {dest_path} (Attempt {attempt + 1}/{max_retries})")
            shutil.move(filepath, dest_path)
            logging.info(f"Successfully moved {filename} to {dest_path}")
            break
        except PermissionError as e:
            logging.warning(f"PermissionError moving {filename}: {e}. Retrying in 1s...")
            time.sleep(1)
        except Exception as e:
            logging.error(f"Error moving file {filename}: {e}")
            # Try copy and delete as fallback
            try:
                shutil.copy2(filepath, dest_path)
                os.remove(filepath)
                logging.info(f"Fallback: Copied and removed {filename} to {dest_path}")
                break
            except Exception as e2:
                logging.error(f"Critical Error moving file {filename}: {e2}")
                if attempt == max_retries - 1:
                    return f"Error: Could not move file - {e2}"
                time.sleep(1)
    
    # 4. Save Extracted Data
    data = {
        "filename": filename,
        "original_path": filepath,
        "destination_path": dest_path,
        "category": category,
        "content": content,
        "processed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    json_filename = f"{os.path.splitext(filename)[0]}.json"
    json_path = os.path.join(EXTRACTED_DIR, json_filename)
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving JSON metadata: {e}")

    return category

@app.route('/', methods=['GET'])
def index():
    # Read processed data for dashboard
    extracted_files = [f for f in os.listdir(EXTRACTED_DIR) if f.endswith('.json')]
    data = []
    for f in extracted_files:
        try:
            with open(os.path.join(EXTRACTED_DIR, f), 'r', encoding='utf-8') as json_file:
                data.append(json.load(json_file))
        except Exception:
            pass
    
    # Group by category
    grouped = {}
    for item in data:
        cat = item.get('category', 'Uncertain')
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(item)
        
    return render_template('index.html', grouped_docs=grouped)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(INPUT_DIR, filename)
        file.save(filepath)
        
        # Trigger processing immediately
        category = process_file(filepath, filename)
        flash(f'File uploaded and classified as: {category}')
        return redirect(url_for('index'))

if __name__ == "__main__":
    setup_directories()
    app.run(debug=True, port=5000)
