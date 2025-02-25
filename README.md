# BioLearn Web Interface

A web-based interface for the BioLearn Python library that allows users to upload methylation data and obtain analysis scores through an intuitive UI.

## Features

- File upload interface for CSV files containing methylation matrices
- Asynchronous processing of uploaded files
- RESTful API for managing samples and retrieving results
- Status tracking for uploaded samples
- Error handling and validation

## Technical Stack

### Backend
- FastAPI (Python web framework)
- Celery (Asynchronous task queue)
- Redis (Message broker and result backend)
- PostgreSQL (Database)
- SQLAlchemy (ORM)

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis

### Environment Setup

1. Create a PostgreSQL database:
```bash
createdb biolearn
```

2. Install dependencies:
```bash
pdm install
```

3. Set up environment variables (optional):
```bash
export REDIS_URL="redis://localhost:6379/0"
export DATABASE_URL="postgresql://postgres:postgres@localhost/biolearn"
```

### Running the Application

1. Start Redis server:
```bash
redis-server
```

2. Start Celery worker:
```bash
cd backend
celery -A app.core.celery_app worker --loglevel=info
```

3. Start the FastAPI server:
```bash
cd backend
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `POST /api/upload` - Upload a methylation data file
- `GET /api/samples` - List all samples
- `GET /api/samples/{sample_id}` - Get details of a specific sample
- `PUT /api/samples/{sample_id}` - Update sample details

## File Format

The application accepts CSV files containing methylation matrices. The expected format is:
- Each row represents a sample
- Each column represents a methylation site
- Values should be between 0 and 1

## Error Handling

The application includes comprehensive error handling for:
- Invalid file formats
- Processing failures
- Database errors
- File system errors

## Security Considerations

- Input validation for all file uploads
- Rate limiting on API endpoints
- Secure file storage with cleanup
- CORS configuration for frontend integration 