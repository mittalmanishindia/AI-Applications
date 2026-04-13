import os
import shutil
import json
import time
import logging
import datetime
from pathlib import Path
import re
from collections import Counter

# Library imports with error handling for optional dependencies
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
WEB_DIR = os.path.join(PROJECT_ROOT, 'web')
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'activity.log')

# Classification Keywords (Simple Semantic Engine)
KEYWORDS = {
    "Invoice": ["invoice", "bill", "total", "amount due", "payment", "tax", "receipt"],
    "Contract": ["agreement", "contract", "parties", "witnesseth", "signature", "terms", "condition"],
    "Report": ["report", "summary", "analysis", "conclusion", "overview", "status", "results"],
    "Form": ["form", "application", "name:", "date:", "dob", "gender", "fill"],
    "Technical": ["code", "software", "system", "specification", "requirement", "api", "data"]
}

def setup_directories():
    """Creates the necessary directory structure."""
    dirs = [INPUT_DIR, PROJECT_ROOT, CLASSES_DIR, EXTRACTED_DIR, WEB_DIR, LOG_DIR]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    # Setup Logging
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

def extract_text_from_pdf(filepath):
    """Extracts text from PDF using pdfplumber (and OCR fallback if needed/configured)."""
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
    
    # Simple OCR fallback check (if text is empty and tesseract is available)
    if not text.strip() and pytesseract and Image:
        try:
            # Note: This requires poppler and tesseract installed on the system
            # For this agent, we might skip complex PDF->Image conversion to avoid external dep issues
            # unless explicitly requested. We will log a warning.
            logging.warning(f"No text found in {filepath}. OCR might be needed but requires system dependencies (Poppler/Tesseract).")
        except Exception:
            pass
            
    return text

def extract_text_from_docx(filepath):
    """Extracts text from DOCX."""
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
    """Extracts text from Images using OCR."""
    text = ""
    if pytesseract and Image:
        try:
            text = pytesseract.image_to_string(Image.open(filepath))
        except Exception as e:
            logging.error(f"Error OCRing image {filepath}: {e}")
            logging.error("Ensure Tesseract-OCR is installed and in your PATH.")
    return text

def extract_text_from_txt(filepath):
    """Extracts text from TXT."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error reading TXT {filepath}: {e}")
        return ""

def classify_document(text):
    """Classifies document based on keyword frequency."""
    text_lower = text.lower()
    scores = Counter()
    
    for category, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                scores[category] += 1
    
    if not scores:
        return "Uncertain"
    
    best_match = scores.most_common(1)[0]
    # Simple threshold
    if best_match[1] >= 1:
        return best_match[0]
    return "Uncertain"

def generate_webpage():
    """Generates a static HTML page with the extracted data."""
    extracted_files = [f for f in os.listdir(EXTRACTED_DIR) if f.endswith('.json')]
    data = []
    
    for f in extracted_files:
        try:
            with open(os.path.join(EXTRACTED_DIR, f), 'r', encoding='utf-8') as json_file:
                data.append(json.load(json_file))
        except Exception as e:
            logging.error(f"Error reading JSON {f}: {e}")

    # Group by category
    grouped = {}
    for item in data:
        cat = item.get('category', 'Uncertain')
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(item)

    # HTML Template
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document Classifier Dashboard</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 20px; }
            h1 { text-align: center; color: #2c3e50; }
            .container { max-width: 1200px; margin: 0 auto; }
            .category-section { margin-bottom: 40px; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .category-title { border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-bottom: 20px; color: #3498db; }
            .document-card { border: 1px solid #eee; padding: 15px; margin-bottom: 15px; border-radius: 4px; transition: all 0.3s ease; }
            .document-card:hover { box-shadow: 0 5px 15px rgba(0,0,0,0.1); transform: translateY(-2px); }
            .doc-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
            .doc-name { font-weight: bold; font-size: 1.1em; }
            .doc-date { color: #888; font-size: 0.9em; }
            .doc-preview { background: #f9f9f9; padding: 10px; border-radius: 4px; font-family: monospace; white-space: pre-wrap; max-height: 150px; overflow-y: auto; font-size: 0.9em; color: #555; }
            .refresh-note { text-align: center; color: #777; margin-top: 40px; font-size: 0.9em; }
        </style>
        <meta http-equiv="refresh" content="10"> <!-- Auto-refresh every 10 seconds -->
    </head>
    <body>
        <div class="container">
            <h1>Document Classification Dashboard</h1>
            <div id="content">
    """
    
    for category, docs in grouped.items():
        html_content += f'<div class="category-section"><h2 class="category-title">{category} ({len(docs)})</h2>'
        for doc in docs:
            # Truncate preview
            preview = doc.get('content', '')[:500] + "..." if len(doc.get('content', '')) > 500 else doc.get('content', '')
            html_content += f"""
            <div class="document-card">
                <div class="doc-header">
                    <span class="doc-name">{doc.get('filename')}</span>
                    <span class="doc-date">{doc.get('processed_at')}</span>
                </div>
                <div class="doc-preview">{preview}</div>
            </div>
            """
        html_content += '</div>'

    html_content += """
            </div>
            <p class="refresh-note">Auto-refreshing every 10 seconds...</p>
        </div>
    </body>
    </html>
    """

    with open(os.path.join(WEB_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)
    logging.info("Webpage updated.")

def process_file(filename):
    """Main processing logic for a single file."""
    filepath = os.path.join(INPUT_DIR, filename)
    if not os.path.isfile(filepath):
        return

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
        logging.warning(f"Unsupported file type: {filename}")
        return

    # 2. Classify
    category = classify_document(content)
    logging.info(f"Classified {filename} as {category}")

    # 3. Move File
    dest_folder = os.path.join(CLASSES_DIR, category)
    os.makedirs(dest_folder, exist_ok=True)
    dest_path = os.path.join(dest_folder, filename)
    
    # Handle duplicate names
    if os.path.exists(dest_path):
        base, extension = os.path.splitext(filename)
        timestamp = int(time.time())
        dest_path = os.path.join(dest_folder, f"{base}_{timestamp}{extension}")
    
    shutil.move(filepath, dest_path)
    
    # 4. Save Extracted Data
    data = {
        "filename": filename,
        "original_path": filepath,
        "category": category,
        "content": content,
        "processed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    json_filename = f"{os.path.splitext(filename)[0]}.json"
    json_path = os.path.join(EXTRACTED_DIR, json_filename)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    logging.info(f"Finished processing {filename}")

def run_batch():
    """Runs the batch processing on the input directory."""
    files = os.listdir(INPUT_DIR)
    if not files:
        logging.info("No files in input directory.")
        return

    for f in files:
        process_file(f)
    
    generate_webpage()

if __name__ == "__main__":
    setup_directories()
    print(f"Agent initialized. Monitoring {INPUT_DIR}...")
    print("Press Ctrl+C to stop.")
    
    # Initial run
    run_batch()
    
    # Simple polling loop for autonomy
    try:
        while True:
            time.sleep(5)
            if os.listdir(INPUT_DIR):
                run_batch()
    except KeyboardInterrupt:
        print("Stopping agent...")
