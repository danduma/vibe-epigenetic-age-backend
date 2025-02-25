from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class ProcessingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETE = "complete"
    ERROR = "error"

class Sample(Base):
    __tablename__ = "samples"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    upload_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(SQLEnum(ProcessingStatus), default=ProcessingStatus.PENDING, nullable=False)
    result = Column(JSON, nullable=True)  # Store all clock results as JSON
    error_message = Column(String, nullable=True)
    analysis_metadata = Column(JSON, nullable=True)
    config = Column(JSON, nullable=True)  # Store analysis configuration

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "upload_timestamp": self.upload_timestamp.isoformat(),
            "status": self.status.value,
            "result": self.result,
            "error_message": self.error_message,
            "analysis_metadata": self.analysis_metadata,
            "config": self.config
        } 