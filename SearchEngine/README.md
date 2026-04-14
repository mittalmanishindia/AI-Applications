# SearchEngine

A simple, lightweight mock search engine built with Flask. This application demonstrates a basic search implementation with a RESTful API and a frontend interface.

## Features

- **Mock Search Functionality**: simulation of search results using a predefined dataset.
- **REST API**: specific endpoint (`/api/search`) to handle search queries asynchronously.
- **Responsive Interface**: Simple and clean user interface for entering queries and viewing results.
- **Real-time Filtering**: Filters results based on title and snippet matching.

## Tech Stack

- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS, JavaScript
- **Data**: In-memory mock data structure

## Prerequisites

Before running the application, ensure you have Python installed on your system.

## Setup and Installation

1.  **Clone or Download the Repository**:
    Navigate to the project directory:
    ```bash
    cd SearchEngine
    ```

2.  **Create a Virtual Environment (Optional but Recommended)**:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    You need to install Flask.
    ```bash
    pip install flask
    ```

## Usage

1.  **Run the Application**:
    Execute the `app.py` script:
    ```bash
    python app.py
    ```

2.  **Access the Search Engine**:
    Open your web browser and go to:
    `http://127.0.0.1:8000`

3.  **Search**:
    Type a keyword (e.g., "AI", "Python", "Travel") into the search bar to see filtered results.

## Project Structure

```
SearchEngine/
├── app.py              # Main Flask application file
├── static/             # Static assets (CSS, JS, Images)
├── templates/
│   └── index.html      # Main HTML template
└── README.md           # Project documentation
```

## Customization

To modify the mock data, edit the `MOCK_RESULTS` list in `app.py`. You can add more dictionaries with `title`, `url`, and `snippet` keys to expand the searchable dataset.
