# FastAPI File Upload Service

A FastAPI-based web service that handles file uploads with validation and rate limiting.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
git clone <repository-url>
cd <project-directory>

2. Create and activate a virtual environment:

Windows
python -m venv venv
.\venv\Scripts\activate

macOS/Linux
python -m venv venv
source venv/bin/activate

3. Install dependencies:
pip install -r requirements.txt

4. Create a `.env` file in the root directory with the following variables:
UPLOAD_FOLDER=uploads
API_KEY=GEMINI-API-KEY


## Running the Application

Optional
Change directory to virtual environment

Windows
venve\Scripts\activate


1. Start the server:
uvicorn app.main:app --reload

The `--reload` flag enables auto-reloading on code changes (recommended for development)

2. Access the API:
- API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

## Features

- File upload handling
- File validation middleware
- Rate limiting middleware
- Configurable upload directory
- Logging system

## Project Structure

app/
├── config/
│ └── config.py # Application configuration
├── middlewares/
│ ├── file_validation.py
│ └── rate_limit.py
├── routers/
│ └── file_router.py # API routes
└── main.py # Application entry point


## API Documentation

Once the server is running, visit http://localhost:8000/docs for detailed API documentation and testing interface.

### Upload a PDF File
Request using CURL (-H option is optional)
curl -X POST "http://localhost:8000/v1/pdf" \
-H "accept: application/json" \
-H "Content-Type: multipart/form-data" \
-F "file=@/path/to/your/document.pdf"

Response in JSON
{
"pdf_id": "abc123...",
"filename": "document.pdf",
"size": 12345,
"upload_time": "2024-03-14T12:00:00"
}


### Chat About a PDF
Request using CURL (-H option is optional)
curl -X POST "http://localhost:8000/v1/chat/{pdf_id}" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d '{
"message": "What is the main topic of this document?"
}'

Response in JSON
{
"response": "Based on the document content, the main topic is...",
"timestamp": "2024-03-14T12:01:00"
}