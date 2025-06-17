from typing import Dict, Any, List, Optional, TypedDict
from datetime import datetime
from enum import Enum

class MigrationStatus(Enum):
    PENDING = "pending"
    STARTED = "started"
    ANALYZING = "analyzing"
    MAPPING = "mapping"
    VALIDATING = "validating"
    SAVING = "saving"
    COMPLETED = "completed"
    FAILED = "failed"

class QualityMetrics(TypedDict):
    """Metrics để đánh giá chất lượng migration"""
    total_questions: int
    successfully_mapped: int
    failed_mappings: int
    validation_errors: List[str]
    quality_score: float  # 0-100
    processing_time: float  # seconds

class MigrationState(TypedDict):
    """State object cho LangGraph migration workflow"""
    
    # Process metadata
    migrate_process_id: int
    user_id: str
    status: MigrationStatus
    current_step: str
    started_at: datetime
    
    # Input data
    raw_input_data: Dict[str, Any]
    quiz_type: str  # "reading" or "listening"
    
    # Processing results
    analyzed_data: Optional[Dict[str, Any]]
    mapped_data: Optional[Dict[str, Any]]
    validated_data: Optional[Dict[str, Any]]
    final_result: Optional[Dict[str, Any]]
    
    # Quality tracking
    quality_metrics: QualityMetrics
    
    # Error handling
    errors: List[str]
    warnings: List[str]
    retry_count: int
    max_retries: int
    
    # Progress tracking
    progress_percentage: float
    current_part_index: int
    total_parts: int
    
    # Configuration
    config: Dict[str, Any]
    
    # Logs for debugging
    processing_logs: List[Dict[str, Any]] 