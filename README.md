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

## Project Overview

- Everything lies under app/
- app/config.config.py # Application configuration
- app/middlewares/file_validation.py # Does file type checking
- app/middlewares/rate_limit.py # Does rate limiting
- app/routers/file_router.py # API routes /** @todo : must seperate chat from file
- app/controllers/file_controller.py # Request to file layer
- app/managers/pdf_manager.py # File data sync after crashes
- app/services/file_service.py # File to OS layer
- app/service/gemini_service.py # File to Gemini layer
- app/utils/pdf_extractor.py # File reads
- app/main.py # Application entry point
- test # Tests lies here
- test/integration # Basic integration test
- test/confext.py # Data for tests
- test/test_chat.py # test chat
- test/test_file_upload.pt # test file upload
- test/test_utils.py # test utils
- setup.py # Package maker
- pytest.ini # test entry file
- uploads/ # Uploaded files will appear here
- .gitignore # Ignored files defined
- pdf_metadata.json # Check pdf_manager.py
- requirements.txt # For builds with same packages
- README.md # Description of how

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
Request using CURL (-H option is must)
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

## Tests
# Run all tests (Assuming in venv)
pytest

# Run with coverage report
pytest --cov=app tests/

# Run specific test file
pytest tests/test_file_upload.py

# Run tests with detailed output
pytest -v

# To run the tests locally, you can use:
pytest tests/unit/ for unit tests
pytest tests/integration/ -m integration for integration tests
pytest for all tests

# Github Actions is just for cosmetics of it.


## Problems to tackle (Bonus Points)
Problems are answered in a a seperate file called PROBLEMS.md to not distract file contents.