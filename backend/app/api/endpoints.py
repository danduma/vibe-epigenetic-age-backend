import os
import json
import uuid
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import List, Optional
import shutil
from ..schemas.sample import ClockType
from ..core.analysis import process_methylation_data  # We'll create this next

router = APIRouter()

# Directory structure
BASE_DIR = "data"
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
METADATA_DIR = os.path.join(BASE_DIR, "metadata")

# Create necessary directories
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)

def save_metadata(sample_id: str, metadata: dict):
    """Save sample metadata to a JSON file"""
    metadata_path = os.path.join(METADATA_DIR, f"{sample_id}.json")
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

def load_metadata(sample_id: str) -> dict:
    """Load sample metadata from JSON file"""
    metadata_path = os.path.join(METADATA_DIR, f"{sample_id}.json")
    try:
        with open(metadata_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Sample not found")

def list_samples() -> List[dict]:
    """List all samples from metadata directory"""
    samples = []
    for filename in os.listdir(METADATA_DIR):
        if filename.endswith('.json'):
            sample_id = filename[:-5]  # Remove .json
            try:
                metadata = load_metadata(sample_id)
                samples.append(metadata)
            except:
                continue
    return samples

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    imputation_strategy: str = Form("mean"),
    normalize_data: bool = Form(True)
):
    """Upload and process a methylation data file"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    # Generate unique ID for this sample
    sample_id = str(uuid.uuid4())
    
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, f"{sample_id}.csv")
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

    # Create metadata
    metadata = {
        "id": sample_id,
        "original_filename": file.filename,
        "upload_timestamp": datetime.utcnow().isoformat(),
        "status": "processing",
        "config": {
            "imputation_strategy": imputation_strategy,
            "normalize_data": normalize_data
        }
    }
    save_metadata(sample_id, metadata)

    try:
        # Process the file synchronously
        result = process_methylation_data(
            file_path=file_path,
            imputation_strategy=imputation_strategy,
            normalize_data=normalize_data
        )
        
        # Update metadata with results
        metadata.update({
            "status": "complete",
            "result": result,
            "completion_timestamp": datetime.utcnow().isoformat()
        })
        save_metadata(sample_id, metadata)
        
        return metadata
    except Exception as e:
        # Update metadata with error
        metadata.update({
            "status": "error",
            "error": str(e),
            "completion_timestamp": datetime.utcnow().isoformat()
        })
        save_metadata(sample_id, metadata)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/samples")
def get_samples(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None
):
    """Get list of all samples with optional status filter"""
    samples = list_samples()
    
    # Filter by status if specified
    if status:
        samples = [s for s in samples if s.get("status") == status]
    
    # Apply pagination
    start = min(skip, len(samples))
    end = min(skip + limit, len(samples))
    
    return samples[start:end]

@router.get("/samples/{sample_id}")
def get_sample(sample_id: str):
    """Get details of a specific sample"""
    return load_metadata(sample_id)

@router.get("/samples/{sample_id}/result")
def get_sample_result(sample_id: str):
    """Get analysis results for a sample"""
    metadata = load_metadata(sample_id)
    
    if metadata["status"] != "complete":
        raise HTTPException(
            status_code=400, 
            detail=f"Sample processing is in status: {metadata['status']}"
        )
    
    return metadata.get("result") 