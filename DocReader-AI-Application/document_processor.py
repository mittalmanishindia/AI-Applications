import os
import logging
from datetime import datetime
import PyPDF2
import docx
import markdown

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

    def get_file_metadata(self, filename):
        """Extracts metadata from the file."""
        filepath = os.path.join(self.upload_folder, filename)
        if not os.path.exists(filepath):
            return None
        
        stat = os.stat(filepath)
        return {
            'filename': filename,
            'size': stat.st_size,
            'upload_date': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'extension': filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        }

    def process_document(self, filename):
        """Reads and extracts text from the document based on its extension."""
        filepath = os.path.join(self.upload_folder, filename)
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        content = ""
        try:
            if ext == 'pdf':
                content = self._read_pdf(filepath)
            elif ext == 'docx':
                content = self._read_docx(filepath)
            elif ext == 'txt':
                content = self._read_txt(filepath)
            elif ext == 'md':
                content = self._read_md(filepath)
            else:
                raise ValueError(f"Unsupported file format: {ext}")
            
            word_count = len(content.split())
            return {
                'content': content,
                'word_count': word_count,
                'success': True
            }
        except Exception as e:
            logger.error(f"Error processing {filename}: {str(e)}")
            return {
                'content': "",
                'word_count': 0,
                'success': False,
                'error': str(e)
            }

    def _read_pdf(self, filepath):
        text = ""
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n\n"
        return text

    def _read_docx(self, filepath):
        doc = docx.Document(filepath)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return "\n\n".join(text)

    def _read_txt(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()

    def _read_md(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            md_content = file.read()
            # Convert Markdown to HTML for display, or keep as text? 
            # Requirement says "Extract text content". 
            # But for display on web page, converting to HTML is better.
            # However, the prompt asks to "Extract text content". 
            # Let's return the raw markdown text here, and we can render it in the template or convert it there.
            # Actually, for consistency with other formats which return raw text, let's return raw text.
            # But wait, if we want "formatted content", maybe we should convert everything to HTML?
            # The prompt says "Display formatted content".
            # Let's stick to extracting text here. The view can handle rendering (e.g., using a markdown filter).
            return md_content
