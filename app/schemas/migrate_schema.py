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

class PartMigrateRequest(BaseModel):
    """Schema cho request migrate từng part riêng biệt"""
    
    # Quiz metadata để biết part thuộc quiz nào
    quiz_id: str = Field(..., description="ID của quiz gốc")
    quiz_title: str = Field(..., description="Tiêu đề quiz")
    quiz_type: str = Field(..., description="Loại quiz (reading/listening)")
    quiz_time: Optional[int] = Field(None, description="Thời gian làm quiz tổng")
    quiz_description: Optional[str] = Field(None, description="Mô tả quiz")
    listening_file_id: Optional[str] = Field(None, description="ID file audio cho listening quiz")
    
    # Part data
    part_index: int = Field(..., description="Chỉ số part (1, 2, 3)")
    part_title: str = Field(..., description="Tiêu đề part")
    part_content: Optional[str] = Field(None, description="Nội dung part (passage)")
    part_description: Optional[str] = Field(None, description="Mô tả part")
    part_time: Optional[int] = Field(None, description="Thời gian làm part")
    questions: List[Dict[str, Any]] = Field(..., description="Danh sách câu hỏi trong part")
    
    # Metadata
    total_parts: int = Field(..., description="Tổng số parts trong quiz")
    user_id: str = Field(..., description="ID người dùng tạo request")

class PartMigrateResponse(BaseModel):
    """Schema cho response migrate từng part"""
    
    part_migrate_id: str = Field(..., description="ID của part migration process")
    quiz_id: str = Field(..., description="ID quiz gốc")
    part_index: int = Field(..., description="Chỉ số part")
    status: str = Field(..., description="Trạng thái migrate (processing/completed/failed)")
    progress_percentage: float = Field(..., description="Phần trăm hoàn thành")
    
    # Kết quả migrate part
    migrated_part: Optional[Dict[str, Any]] = Field(None, description="Dữ liệu part đã migrate")
    migrated_question_sets: Optional[List[Dict[str, Any]]] = Field(None, description="Question sets đã migrate")
    migrated_questions: Optional[List[Dict[str, Any]]] = Field(None, description="Questions đã migrate")
    
    # Metadata
    created_at: datetime = Field(..., description="Thời gian tạo")
    completed_at: Optional[datetime] = Field(None, description="Thời gian hoàn thành")
    error_message: Optional[str] = Field(None, description="Thông báo lỗi nếu có")

class QuizMergeRequest(BaseModel):
    """Schema cho request merge các parts thành quiz hoàn chỉnh"""
    
    quiz_id: str = Field(..., description="ID quiz gốc")
    part_migrate_ids: List[str] = Field(..., description="Danh sách IDs của part migrations")
    user_id: str = Field(..., description="ID người dùng")

class QuizMergeResponse(BaseModel):
    """Schema cho response merge quiz hoàn chỉnh"""
    
    quiz_merge_id: str = Field(..., description="ID của quiz merge process")
    quiz_id: str = Field(..., description="ID quiz gốc")
    status: str = Field(..., description="Trạng thái merge (processing/completed/failed)")
    
    # Kết quả final
    final_quiz: Optional[Dict[str, Any]] = Field(None, description="Quiz hoàn chỉnh đã merge")
    total_parts: int = Field(..., description="Tổng số parts đã merge")
    total_question_sets: int = Field(..., description="Tổng số question sets")
    total_questions: int = Field(..., description="Tổng số questions")
    
    # Metadata
    created_at: datetime = Field(..., description="Thời gian bắt đầu merge")
    completed_at: Optional[datetime] = Field(None, description="Thời gian hoàn thành merge")
    error_message: Optional[str] = Field(None, description="Thông báo lỗi nếu có") 