# backend/models/schemas.py

from pydantic import BaseModel, Field, HttpUrl, validator
from typing import List, Dict, Optional, Union
from datetime import datetime
from enum import Enum

class ContentType(str, Enum):
    FINANCIAL_REPORT = "financial_report"
    NEWS_ARTICLE = "news_article"
    PRESS_RELEASE = "press_release"
    REGULATORY_FILING = "regulatory_filing"
    COMPANY_WEBSITE = "company_website"
    OTHER = "other"

class SearchResult(BaseModel):
    question: str
    organization: str
    content: str
    url: str
    content_type: Optional[ContentType] = ContentType.OTHER
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    relevance_score: Optional[float] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class QueryRequest(BaseModel):
    questions: List[str] = Field(..., min_items=1, max_items=10)
    organizations: List[str] = Field(..., min_items=1, max_items=10)
    
    @validator('questions')
    def validate_questions(cls, v):
        if not all(q.strip() for q in v):
            raise ValueError("Questions cannot be empty strings")
        return [q.strip() for q in v]
    
    @validator('organizations')
    def validate_organizations(cls, v):
        if not all(org.strip() for org in v):
            raise ValueError("Organizations cannot be empty strings")
        return [org.strip() for org in v]

class AnalysisResult(BaseModel):
    answer: str
    key_findings: List[str]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    sources: List[HttpUrl]
    relevant_quotes: Optional[List[str]] = None
    metadata: Dict = Field(default_factory=dict)

class QueryResponse(BaseModel):
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    results: Dict[str, Dict[str, AnalysisResult]]  # {question: {organization: result}}
    error: Optional[str] = None
    processing_time: float
    total_sources_analyzed: int

class VectorRecord(BaseModel):
    id: str
    values: List[float]
    metadata: Dict[str, Union[str, float, datetime]]

class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class AsyncQueryResponse(BaseModel):
    request_id: str
    status: ProcessingStatus
    estimated_completion_time: Optional[datetime]
    results_url: Optional[HttpUrl] = None
    error: Optional[str] = None

# Export all models
__all__ = [
    'ContentType',
    'SearchResult',
    'QueryRequest',
    'AnalysisResult',
    'QueryResponse',
    'VectorRecord',
    'ProcessingStatus',
    'AsyncQueryResponse'
]