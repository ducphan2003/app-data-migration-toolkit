from pydantic import BaseModel, Field
from typing import Optional, Dict, Union
from enum import Enum

class MigrationStatus(str, Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'

class MigrateQuizSchema(BaseModel):
    quiz_id: str = Field(..., min_length=1, description="ID của quiz cần migrate")

class MigrationStatusSchema(BaseModel):
    process_id: str = Field(..., description="ID của quá trình migrate")
    status: MigrationStatus = Field(..., description="Trạng thái của quá trình migrate")
    progress: float = Field(..., description="Tiến độ migrate (0-100%)")
    message: Optional[str] = Field(None, description="Thông báo về quá trình migrate")
    result: Optional[Dict] = Field(None, description="Kết quả migrate")

    class Config:
        use_enum_values = True 