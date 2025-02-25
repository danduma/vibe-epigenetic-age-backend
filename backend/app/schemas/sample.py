from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from enum import Enum
from ..models.sample import ProcessingStatus

class ClockType(str, Enum):
    HORVATH = "horvath"
    HANNUM = "hannum"
    PHENOAGE = "phenoage"

class ClockResult(BaseModel):
    predicted_age: float
    std_predicted_age: float
    num_samples: int
    individual_predictions: List[float]

class ClockError(BaseModel):
    error: str

class AnalysisConfig(BaseModel):
    imputation_strategy: str = Field(default="mean", description="Strategy for handling missing CpG sites")
    normalize_data: bool = Field(default=True, description="Whether to normalize the methylation data")

class AnalysisResult(BaseModel):
    clocks: Dict[ClockType, Union[ClockResult, ClockError]]
    total_sites_used: int
    config: AnalysisConfig

class SampleBase(BaseModel):
    filename: str
    analysis_metadata: Optional[Dict[str, Any]] = None
    config: Optional[AnalysisConfig] = None

class SampleCreate(SampleBase):
    pass

class SampleResponse(SampleBase):
    id: int
    upload_timestamp: datetime
    status: ProcessingStatus
    result: Optional[AnalysisResult] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True

class SampleUpdate(BaseModel):
    status: Optional[ProcessingStatus] = None
    result: Optional[AnalysisResult] = None
    error_message: Optional[str] = None
    analysis_metadata: Optional[Dict[str, Any]] = None
    config: Optional[AnalysisConfig] = None 