from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

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

class CreateMigrateProcessSchema(BaseModel):
    id: int = Field(..., description="ID của quiz cần migrate")
    title: str = Field(..., description="Tiêu đề của quiz")
    type: Optional[int] = Field(None, description="Loại quiz (1=reading, 2=listening)")
    time: Optional[int] = Field(None, description="Thời gian làm bài (phút)")
    description: Optional[str] = Field(None, description="Mô tả quiz")
    listening: Optional[str] = Field(None, description="File audio cho listening")
    parts: List[Dict[str, Any]] = Field(..., description="Danh sách parts của quiz")

class MigrateProcessResponseSchema(BaseModel):
    id: int = Field(..., description="ID của migrate process")
    quiz_id: str = Field(..., description="ID của quiz được migrate")
    status: str = Field(..., description="Trạng thái tổng thể")
    prepare_data_status: str = Field(..., description="Trạng thái step 1")
    mapping_structure_status: str = Field(..., description="Trạng thái step 2")
    validate_data_status: str = Field(..., description="Trạng thái step 3")
    error_message: Optional[str] = Field(None, description="Thông báo lỗi nếu có")
    user_created: str = Field(..., description="User tạo")
    date_created: str = Field(..., description="Ngày tạo")
    date_updated: Optional[str] = Field(None, description="Ngày cập nhật cuối")
    prepare_data_result: Optional[Dict[str, Any]] = Field(None, description="Kết quả step 1")
    mapping_structure_result: Optional[Dict[str, Any]] = Field(None, description="Kết quả step 2")
    validate_data_result: Optional[Dict[str, Any]] = Field(None, description="Kết quả step 3")
    final_result: Optional[Dict[str, Any]] = Field(None, description="Kết quả cuối cùng") 