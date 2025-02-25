# BioLearn Web Interface

A web-based interface for the BioLearn Python library that allows users to upload methylation data and obtain epigenetic clock analysis scores through an intuitive UI.

## Features

- File upload interface for CSV files containing methylation matrices
- Asynchronous processing of uploaded files
- RESTful API for managing samples and retrieving results
- Status tracking for uploaded samples
- Error handling and validation
- Support for multiple epigenetic clocks (Horvath, Hannum, PhenoAge)
- Statistical analysis of methylation data

## Technical Stack

### Backend
- FastAPI (Python web framework)
- BioLearn Python library (v0.7.0+)
- Pydantic for data validation

## Setup

### Prerequisites

- Python 3.10
- PDM (Python dependency manager)

### Environment Setup

1. Install dependencies:
```bash
pdm install
```

### Running the Application

1. Start the FastAPI server:
```bash
cd backend
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `POST /api/upload` - Upload a methylation data file with configuration options
- `GET /api/samples` - List all samples with optional pagination and status filtering
- `GET /api/samples/{sample_id}` - Get details of a specific sample
- `GET /api/samples/{sample_id}/result` - Get analysis results for a specific sample

## File Format

The application accepts CSV files containing methylation matrices. The expected format is:
- Each row represents a CpG site (methylation probe)
- Each column represents a sample
- Values should be beta values between 0 and 1

## Epigenetic Clocks

The application currently supports the following epigenetic clocks:
- Horvath's Clock (2013)
- Hannum's Clock (2013)
- PhenoAge Clock (Levine et al., 2018)

## Error Handling

The application includes comprehensive error handling for:
- Invalid file formats
- Processing failures
- Database errors
- File system errors
- Individual clock failures (other clocks will still run)

## Security Considerations

- Input validation for all file uploads
- Rate limiting on API endpoints
- Secure file storage with cleanup
- CORS configuration for frontend integration
- Authentication and authorization (configured) 