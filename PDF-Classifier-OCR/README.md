# Autonomous AI Document Classifier Agent

This agent autonomously ingests, classifies, extracts content from, and visualizes documents using **Generative AI (LLM)**.

## Features

*   **Web Interface**: Upload documents directly via a Flask-based web UI.
*   **AI Classification**: Uses Google Gemini (or configurable LLM) to semantically understand and classify documents into categories like Invoice, Contract, Report, etc.
*   **Content Extraction**: Extracts text from PDF, DOCX, Images (OCR), and TXT files.
*   **Automated Organization**: Moves files into categorized folders.
*   **Live Dashboard**: View classified documents and their content in real-time.

## Project Structure

```
Agent3- PDF Classifier_OCR/
├── app.py                 # Flask Application & Agent Logic
├── requirements.txt       # Dependencies
├── .env                   # API Keys (Create this from .env.example)
├── templates/
│   └── index.html         # Web Dashboard Template
├── project_root/
│   ├── classes/           # Classified documents
│   ├── extracted/         # JSON metadata
│   └── logs/              # Activity logs
```

## Setup & Usage

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure API Key**:
    *   Rename `.env.example` to `.env`.
    *   Add your Google Gemini API Key: `GEMINI_API_KEY=your_key_here`.
    *   *If no key is provided, the agent falls back to a basic "Uncertain" state.*

3.  **Run the Agent**:
    ```bash
    python app.py
    ```

4.  **Access the Dashboard**:
    Open your browser and go to `http://127.0.0.1:5000`.

5.  **Upload & Classify**:
    Use the "Upload New Document" button to submit files. The agent will process them instantly.
