from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
from uuid import UUID

class QuestionType(str, Enum):
	MATCHING_INFO = "MATCHING_INFO"
	OTHERS = "OTHERS"
	MATCHING_NAMES = "MATCHING_NAMES"
	TRUE_FALSE = "TRUE_FALSE"
	MATCHING_HEADING = "MATCHING_HEADING"
	MAP_DIAGRAM_LABEL = "MAP_DIAGRAM_LABEL"
	MULTIPLE_CHOICE_ONE = "MULTIPLE_CHOICE_ONE"
	MULTIPLE_CHOICE_MANY = "MULTIPLE_CHOICE_MANY"
	YES_NO = "YES_NO"
	FILL_BLANK = "FILL_BLANK"

class QuestionSetType(str, Enum):
    GAP_FILLING = "GAP_FILLING"
    SINGLE_SELECTION = "SINGLE_SELECTION"
    SINGLE_CHOICE = "SINGLE_CHOICE"
    MATCHING = "MATCHING"
    NOTE_COMPLETION = "NOTE_COMPLETION"
    MULTIPLE_CHOICE_MANY = "MULTIPLE_CHOICE_MANY"

class QuizType(int, Enum):
    READING_LEGACY = 1
    LISTENING_LEGACY = 2
    READING_V2 = 9
    LISTENING_V2 = 10

class QuestionOptionSchema(BaseModel):
    text: str = Field(..., description="Nội dung của option")
    option: str = Field(..., description="Option")
    is_correct: bool = Field(..., description="Đánh dấu đáp án đúng")

class QuestionSchema(BaseModel):
    title: str = Field(..., description="Tiêu đề câu hỏi")
    question_type: QuestionType = Field(..., description="Loại câu hỏi")
    content: Optional[str] = Field(None, description="Nội dung câu hỏi")
    options: Optional[List[QuestionOptionSchema]] = Field(None, description="Danh sách các lựa chọn")
    correct_answer: Optional[str] = Field(None, description="Đáp án đúng cho câu hỏi single choice")
    correct_answers: Optional[List[str]] = Field(None, description="Danh sách đáp án đúng cho câu hỏi multiple choice")
    listen_from: Optional[int] = Field(None, description="Thời điểm bắt đầu audio (cho listening)")
    explain: Optional[str] = Field(None, description="Giải thích đáp án dạng HTML")
    sort: int = Field(..., description="Thứ tự câu hỏi")
    time_limit: Optional[int] = Field(30, description="Thời gian làm bài (giây)")
    locate_info: Optional[Dict[str, Any]] = Field(None, description="Thông tin vị trí")
    status: str = Field("published", description="Trạng thái câu hỏi")
    type: Optional[str] = Field(None, description="Loại câu hỏi (legacy)")
    single_choice_radio: Optional[Dict[str, Any]] = Field(None, description="Thông tin single choice radio (legacy)")
    selection: Optional[Dict[str, Any]] = Field(None, description="Thông tin selection (legacy)")
    mutilple_choice: Optional[Dict[str, Any]] = Field(None, description="Thông tin multiple choice (legacy)")
    gap_fill_in_blank: Optional[str] = Field(None, description="Thông tin gap fill in blank (legacy)")
    selection_option: Optional[Dict[str, Any]] = Field(None, description="Thông tin selection option (legacy)")
    locate: Optional[str] = Field(None, description="Vị trí câu hỏi")
    order: Optional[int] = Field(None, description="Thứ tự câu hỏi (legacy)")
    description: Optional[str] = Field(None, description="Mô tả câu hỏi")
    content_writing: Optional[str] = Field(None, description="Nội dung writing")
    time_to_think: Optional[int] = Field(None, description="Thời gian suy nghĩ")
    instruction: Optional[str] = Field(None, description="Hướng dẫn làm bài")
    writing_graph_image: Optional[UUID] = Field(None, description="ID ảnh biểu đồ writing")
    writing_graph_description: Optional[str] = Field(None, description="Mô tả biểu đồ writing")
    writing_graph_type: Optional[int] = Field(None, description="Loại biểu đồ writing")
    audio_url: Optional[str] = Field(None, description="URL audio")
    max_words: Optional[int] = Field(None, description="Số từ tối đa")
    min_words: Optional[int] = Field(None, description="Số từ tối thiểu")
    text: Optional[str] = Field(None, description="Nội dung text")

class InstructionSchema(BaseModel):
    id: Optional[int] = Field(None, description="ID của instruction")
    title: str = Field(..., description="Tiêu đề của instruction")
    content: str = Field(..., description="Nội dung của instruction")
    sort: Optional[int] = Field(None, description="Thứ tự của instruction")

class QuestionSetSchema(BaseModel):
    title: str = Field(..., description="Tiêu đề của question set")
    description: str = Field(..., description="Mô tả/hướng dẫn của question set")
    question_type: QuestionSetType = Field(..., description="Loại câu hỏi trong set")
    content: Optional[str] = Field(None, description="Nội dung HTML với placeholders")
    questions: List[QuestionSchema] = Field(..., description="Danh sách câu hỏi")
    options: Optional[List[Dict[str, Any]]] = Field(None, description="Options chung cho cả question set")
    option_title: Optional[str] = Field(None, description="Tiêu đề cho options")
    allow_reuse: Optional[bool] = Field(False, description="Cho phép tái sử dụng options")
    max_selections: Optional[int] = Field(None, description="Số lượng lựa chọn tối đa")
    sort: int = Field(..., description="Thứ tự của question set")

class PartSchema(BaseModel):
    title: str = Field(..., description="Tiêu đề của part")
    content: Optional[str] = Field(None, description="Nội dung của part (passage cho reading)")
    instruction: Optional[InstructionSchema] = Field(None, description="Hướng dẫn cho part")
    file_id: Optional[str] = Field(None, description="ID file audio cho listening part")
    question_sets: List[QuestionSetSchema] = Field(..., description="Danh sách các question set")
    sort: int = Field(..., description="Thứ tự của part")
    passage: Optional[int] = Field(None, description="Số thứ tự passage")
    simplified_content: Optional[str] = Field(None, description="Nội dung đơn giản hóa")
    order: Optional[int] = Field(None, description="Thứ tự của part")
    time: Optional[int] = Field(None, description="Thời gian làm part")
    question_count: Optional[int] = Field(0, description="Số lượng câu hỏi")
    listen_from: Optional[int] = Field(None, description="Thời điểm bắt đầu audio")
    listen_to: Optional[int] = Field(None, description="Thời điểm kết thúc audio")
    task_instruction: Optional[str] = Field(None, description="Hướng dẫn task")
    transcription: Optional[str] = Field(None, description="Thông tin transcription")

class CreateQuizSchema(BaseModel):
    title: str = Field(..., min_length=1, description="Tiêu đề của quiz")
    type: QuizType = Field(..., description="Loại quiz (reading/listening)")
    time: int = Field(..., gt=0, description="Thời gian làm bài (phút)")
    instruction_audio: Optional[str] = Field(None, description="ID file audio hướng dẫn")
    parts: List[PartSchema] = Field(..., min_items=1, description="Danh sách các part")
    is_public: bool = Field(True, description="Quiz có public hay không")
    is_test: bool = Field(True, description="Là bài test hay practice")
    status: str = Field("published", description="Trạng thái của quiz")
    sort: Optional[int] = Field(None, description="Thứ tự của quiz")
    content: Optional[str] = Field(None, description="Nội dung của quiz")
    order: Optional[int] = Field(None, description="Thứ tự của quiz")
    listening: Optional[UUID] = Field(None, description="ID file audio listening")
    description: Optional[str] = Field(None, description="Mô tả quiz")
    instruction: Optional[int] = Field(None, description="ID instruction")
    quiz_code: Optional[str] = Field(None, description="Mã quiz")
    limit_submit: Optional[int] = Field(None, description="Giới hạn số lần nộp bài")
    question: Optional[str] = Field(None, description="Câu hỏi của quiz")
    samples: Optional[str] = Field(None, description="Mẫu câu trả lời")
    thumbnail: Optional[UUID] = Field(None, description="ID ảnh thumbnail")
    vote_count: Optional[int] = Field(0, description="Số lượt vote")
    quiz_type: Optional[int] = Field(None, description="Loại quiz")
    full_id: Optional[int] = Field(None, description="ID đầy đủ")
    mode: Optional[int] = Field(0, description="Chế độ quiz")
    simplified_id: Optional[int] = Field(None, description="ID đơn giản hóa")
    mock_test_id: Optional[int] = Field(None, description="ID mock test")
    mock_test_type: Optional[int] = Field(None, description="Loại mock test")
    total_submitted: Optional[int] = Field(0, description="Tổng số lần nộp bài")
    short_description: Optional[str] = Field(None, description="Mô tả ngắn")
    practice_listing_priority: Optional[int] = Field(0, description="Độ ưu tiên trong danh sách practice")
    writing_task_type: Optional[int] = Field(None, description="Loại task writing")
    meta: Optional[Dict[str, Any]] = Field(None, description="Metadata của quiz")
    prompt_set_id: Optional[int] = Field(None, description="ID prompt set")
    speaking_part_type: Optional[int] = Field(None, description="Loại part speaking")
    speaking_topic_id: Optional[int] = Field(None, description="ID topic speaking")

    @field_validator('parts')
    def validate_parts(cls, v):
        if not v:
            raise ValueError("Quiz phải có ít nhất một part")
        return v

class QuizResponseSchema(BaseModel):
    id: int = Field(..., description="ID của quiz")
    title: str = Field(..., description="Tiêu đề của quiz")
    type: QuizType = Field(..., description="Loại quiz")
    time: int = Field(..., description="Thời gian làm bài")
    status: str = Field(..., description="Trạng thái của quiz")
    is_public: bool = Field(..., description="Quiz có public hay không")
    is_test: bool = Field(..., description="Là bài test hay practice")
    created_at: str = Field(..., description="Thời gian tạo")
    updated_at: Optional[str] = Field(None, description="Thời gian cập nhật cuối") 
