
# DocReader AI Agent

A Python-based AI agent that reads documents (PDF, DOCX, TXT, MD) and publishes their content to a beautiful, responsive web page.

## Features

- **Multi-format Support**: Reads PDF, DOCX, TXT, and Markdown files.
- **Web Interface**: Clean, modern dashboard for uploading and managing documents.
- **Document Reader**: Distraction-free reading mode with formatted content.
- **Metadata Extraction**: Automatically extracts file size, upload date, and word count.
- **Responsive Design**: Works seamlessly on desktop and mobile devices.

## Prerequisites

- Python 3.9 or higher

## Installation

1.  Clone the repository or navigate to the project folder.
2.  Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Start the application:

    ```bash
    python app.py
    ```

2.  Open your web browser and go to:
    `http://127.0.0.1:5000`

3.  Upload a document using the dashboard.
4.  Click the "eye" icon to view the processed content.

## Project Structure

- `app.py`: Main Flask application entry point.
- `document_processor.py`: Logic for reading and processing different file formats.
- `templates/`: HTML templates for the web interface.
- `static/`: CSS styles and other static assets.
- `uploads/`: Directory where uploaded files are stored.
- `requirements.txt`: List of Python dependencies.

## Security Note

This application is designed for local use or controlled environments. It includes basic file type validation and size limits. For production deployment, ensure proper security measures (e.g., HTTPS, authentication) are implemented.
