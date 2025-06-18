import logging
import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.schema import BaseMessage

from app.utils.const import DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE

logger = logging.getLogger(__name__)

# Pydantic models cho structured output
class QuestionTypeAnalysis(BaseModel):
    """Phân tích loại câu hỏi"""
    question_id: str = Field(description="ID của câu hỏi")
    detected_type: str = Field(description="Loại câu hỏi được phát hiện")
    confidence: float = Field(description="Độ tin cậy (0-1)")
    reasoning: str = Field(description="Lý do phân loại")
    key_indicators: List[str] = Field(description="Các dấu hiệu chính")

class QuestionStructure(BaseModel):
    """Cấu trúc question đầy đủ theo database"""
    id: Optional[int] = Field(description="Question ID")
    status: Optional[str] = Field(default="published", description="Question status")
    sort: Optional[int] = Field(description="Sort order")
    user_created: Optional[str] = Field(description="User created")
    date_created: Optional[str] = Field(description="Date created")
    user_updated: Optional[str] = Field(description="User updated")
    date_updated: Optional[str] = Field(description="Date updated")
    title: Optional[str] = Field(description="Question title")
    content: Optional[str] = Field(description="Question content")
    locate: Optional[str] = Field(description="Locate")
    order: Optional[int] = Field(description="Question order")
    explain: Optional[str] = Field(description="Question explanation")
    description: Optional[str] = Field(description="Question description")
    content_writing: Optional[str] = Field(description="Content writing")
    time_to_think: Optional[int] = Field(description="Time to think")
    listen_from: Optional[int] = Field(description="Listen from")
    instruction: Optional[str] = Field(description="Instruction")
    writing_graph_image: Optional[str] = Field(description="Writing graph image")
    writing_graph_description: Optional[str] = Field(description="Writing graph description")
    writing_graph_type: Optional[int] = Field(description="Writing graph type")
    audio_url: Optional[str] = Field(description="Audio URL")
    time_limit: Optional[int] = Field(default=30, description="Time limit")
    max_words: Optional[int] = Field(description="Max words")
    min_words: Optional[int] = Field(description="Min words")
    text: Optional[str] = Field(description="Question text")
    locate_info: Optional[Dict[str, Any]] = Field(description="Locate info")
    quiz_id: Optional[int] = Field(default=0, description="Quiz ID (set to 0)")
    part_id: Optional[int] = Field(description="Part ID (set to null)")
    type: Optional[str] = Field(default="", description="Legacy type field")
    gap_fill_in_blank: Optional[str] = Field(description="Gap fill content (set to null)")
    single_choice_radio: Optional[Dict[str, Any]] = Field(description="Single choice radio (set to null)")
    selection: Optional[Dict[str, Any]] = Field(description="Selection (set to null)")
    mutilple_choice: Optional[Dict[str, Any]] = Field(description="Multiple choice (set to null)")
    selection_option: Optional[Dict[str, Any]] = Field(description="Selection option (set to null)")
    question_set_id: Optional[int] = Field(description="Question set ID")
    question_type: Optional[str] = Field(description="Question type")
    correct_answer: Optional[str] = Field(description="Correct answer (single)")
    correct_answers: Optional[List[str]] = Field(description="Correct answers (multiple)")
    options: Optional[Dict[str, Any]] = Field(description="Question options")

class QuestionSetStructure(BaseModel):
    """Cấu trúc question set đầy đủ theo database"""
    id: Optional[int] = Field(description="Question set ID")
    part_id: Optional[int] = Field(description="Part ID")
    user_created: Optional[str] = Field(description="User created")
    date_created: Optional[str] = Field(description="Date created")
    user_updated: Optional[str] = Field(description="User updated")
    date_updated: Optional[str] = Field(description="Date updated")
    question_type: str = Field(description="Question type (GAP_FILLING, SINGLE_SELECTION, etc.)")
    question_count: int = Field(description="Number of questions")
    title: Optional[str] = Field(description="Question set title")
    description: str = Field(description="Question set description")
    content: Optional[str] = Field(description="Question set content")
    option_title: Optional[str] = Field(description="Option title")
    options: Optional[Dict[str, Any]] = Field(description="Question set options")
    allow_reuse: Optional[bool] = Field(description="Allow option reuse")
    max_selections: Optional[int] = Field(description="Max selections")
    sort: Optional[int] = Field(description="Sort order")

class PartStructure(BaseModel):
    """Cấu trúc part đầy đủ theo database"""
    id: Optional[int] = Field(description="Part ID")
    sort: Optional[int] = Field(description="Sort order")
    user_created: Optional[str] = Field(description="User created")
    date_created: Optional[str] = Field(description="Date created")
    date_updated: Optional[str] = Field(description="Date updated")
    title: Optional[str] = Field(description="Part title")
    order: Optional[int] = Field(description="Part order")
    content: Optional[str] = Field(description="Part content (passage)")
    quiz: Optional[int] = Field(description="Quiz ID")
    time: Optional[int] = Field(description="Part time")
    passage: Optional[int] = Field(default=0, description="Passage number")
    simplified_content: Optional[str] = Field(description="Simplified content")
    question_count: Optional[int] = Field(default=0, description="Question count")
    listen_from: Optional[int] = Field(description="Listen from")
    listen_to: Optional[int] = Field(description="Listen to")
    instruction: Optional[int] = Field(description="Instruction")
    task_instruction: Optional[str] = Field(description="Task instruction")
    transcription: Optional[Dict[str, Any]] = Field(description="Transcription")
    file_id: Optional[str] = Field(description="File ID")

class QuizStructure(BaseModel):
    """Cấu trúc quiz đầy đủ theo database"""
    id: Optional[int] = Field(description="Quiz ID")
    status: Optional[str] = Field(default="published", description="Quiz status")
    sort: Optional[int] = Field(description="Sort order")
    user_created: Optional[str] = Field(description="User created")
    date_created: Optional[str] = Field(description="Date created")
    user_updated: Optional[str] = Field(description="User updated")
    date_updated: Optional[str] = Field(description="Date updated")
    type: Optional[int] = Field(description="Quiz type")
    content: Optional[str] = Field(description="Quiz content")
    title: Optional[str] = Field(description="Quiz title")
    order: Optional[int] = Field(description="Quiz order")
    time: Optional[int] = Field(description="Quiz time")
    description: Optional[str] = Field(description="Quiz description")
    instruction: Optional[int] = Field(description="Instruction")
    quiz_code: Optional[str] = Field(description="Quiz code")
    limit_submit: Optional[int] = Field(description="Limit submit")
    question: Optional[str] = Field(description="Question")
    samples: Optional[str] = Field(description="Samples")
    thumbnail: Optional[str] = Field(description="Thumbnail")
    vote_count: Optional[int] = Field(default=0, description="Vote count")
    quiz_type: Optional[int] = Field(description="Quiz type")
    full_id: Optional[int] = Field(description="Full ID")
    is_test: Optional[bool] = Field(description="Is test")
    mode: Optional[int] = Field(default=0, description="Mode")
    simplified_id: Optional[int] = Field(description="Simplified ID")
    mock_test_id: Optional[int] = Field(description="Mock test ID")
    mock_test_type: Optional[int] = Field(description="Mock test type")
    total_submitted: Optional[int] = Field(default=0, description="Total submitted")
    short_description: Optional[str] = Field(description="Short description")
    practice_listing_priority: Optional[int] = Field(default=0, description="Practice listing priority")
    is_public: Optional[bool] = Field(default=True, description="Is public")
    writing_task_type: Optional[int] = Field(description="Writing task type")
    meta: Optional[Dict[str, Any]] = Field(description="Meta data")
    prompt_set_id: Optional[int] = Field(description="Prompt set ID")
    speaking_part_type: Optional[int] = Field(description="Speaking part type")
    speaking_topic_id: Optional[int] = Field(description="Speaking topic ID")
    listening: Optional[str] = Field(description="Listening (skip)")
    instruction_audio: Optional[str] = Field(description="Instruction audio (skip)")
    tags: Optional[str] = Field(description="Tags")
    extra: Optional[Dict[str, Any]] = Field(description="Extra data")
    speaking_topic: Optional[str] = Field(description="Speaking topic")

class MigrationResult(BaseModel):
    """Kết quả migration đầy đủ"""
    quiz: QuizStructure = Field(description="Quiz data")
    parts: List[PartStructure] = Field(description="Parts data")
    question_sets: List[QuestionSetStructure] = Field(description="Question sets data")
    questions: List[QuestionStructure] = Field(description="Questions data")

class AIMigrationAgents:
    """AI Agents cho migration workflow với multi-provider support"""
    
    def __init__(self, 
                 openrouter_api_key: str = None,
                 gpt_api_key: str = None, 
                 gemini_api_key: str = None,
                 claude_api_key: str = None,
                 provider: str = "openrouter",
                 model: str = "anthropic/claude-sonnet-4"):
        
        self.provider = provider
        self.model = model
        
        # Setup LLM based on available keys
        self.llm = self._setup_llm(
            openrouter_api_key=openrouter_api_key,
            gpt_api_key=gpt_api_key,
            gemini_api_key=gemini_api_key,
            claude_api_key=claude_api_key
        )
        
    def _setup_llm(self, openrouter_api_key=None, gpt_api_key=None, gemini_api_key=None, claude_api_key=None):
        """Setup LLM dựa trên API keys có sẵn"""
        
        # Thử OpenRouter trước (thường có nhiều models)
        if openrouter_api_key and openrouter_api_key.strip():
            try:
                from langchain_openai import ChatOpenAI
                logger.info("Using OpenRouter API with anthropic/claude-sonnet-4")
                return ChatOpenAI(
                    api_key=openrouter_api_key,
                    base_url="https://openrouter.ai/api/v1",
                    model="anthropic/claude-sonnet-4",
                    temperature=DEFAULT_TEMPERATURE,
                    max_tokens=DEFAULT_MAX_TOKENS,
                    request_timeout=60  # 60 seconds timeout cho Claude
                )
            except Exception as e:
                logger.warning(f"Failed to setup OpenRouter: {e}")
        
        # Thử GPT API
        if gpt_api_key and gpt_api_key.strip():
            try:
                from langchain_openai import ChatOpenAI
                logger.info("Using OpenAI GPT API")
                return ChatOpenAI(
                    api_key=gpt_api_key,
                    model="gpt-4o-mini",
                    temperature=DEFAULT_TEMPERATURE,
                    max_tokens=DEFAULT_MAX_TOKENS,
                    request_timeout=30  # 30 seconds timeout
                )
            except Exception as e:
                logger.warning(f"Failed to setup OpenAI GPT: {e}")
        
        # Thử Gemini API
        if gemini_api_key and gemini_api_key.strip():
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                logger.info("Using Google Gemini API")
                return ChatGoogleGenerativeAI(
                    google_api_key=gemini_api_key,
                    model="gemini-1.5-pro",
                    temperature=DEFAULT_TEMPERATURE,
                    max_output_tokens=DEFAULT_MAX_TOKENS
                )
            except Exception as e:
                logger.warning(f"Failed to setup Gemini: {e}")
        
        # Thử Claude API
        if claude_api_key and claude_api_key.strip():
            try:
                from langchain_anthropic import ChatAnthropic
                logger.info("Using Anthropic Claude API")
                return ChatAnthropic(
                    anthropic_api_key=claude_api_key,
                    model="claude-3-5-sonnet-20241022",
                    temperature=DEFAULT_TEMPERATURE,
                    max_tokens=DEFAULT_MAX_TOKENS
                )
            except Exception as e:
                logger.warning(f"Failed to setup Claude: {e}")
        
        # Fallback: Mock LLM cho testing
        logger.warning("No valid API keys found, using Mock LLM for testing")
        return self._create_mock_llm()
    
    def _create_mock_llm(self):
        """Tạo Mock LLM cho testing khi không có API key"""
        # Sử dụng fallback logic thay vì Mock LLM phức tạp
        logger.info("Using fallback logic instead of Mock LLM")
        return None
        
    def _load_structure_rules(self) -> str:
        """Load migration rules từ file"""
        try:
            rules_path = "import-data-tool/prompt/structure-rules.md"
            with open(rules_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("Structure rules file not found, using empty rules")
            return ""
    
    def _load_base_migration_rules(self) -> str:
        """Load base migration rules (Migration rules by object)"""
        try:
            rules_path = "import-data-tool/prompt/base-migration-rules.md"
            with open(rules_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("Base migration rules file not found, using structure rules")
            return self._load_structure_rules()
    
    def _load_question_type_rules(self, question_type: str) -> str:
        """Load rules cho specific question type"""
        try:
            rules_path = f"import-data-tool/prompt/{question_type.lower()}-rules.md"
            with open(rules_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Question type rules file not found for {question_type}, using empty rules")
            return ""
    
    def _group_questions_by_type(self, questions: List[Dict[str, Any]], question_analyses: List[QuestionTypeAnalysis]) -> Dict[str, List[Dict[str, Any]]]:
        """Group questions theo question type để migrate riêng biệt"""
        grouped = {}
        
        # Create mapping từ question_id đến analysis
        analysis_map = {analysis.question_id: analysis for analysis in question_analyses}
        
        for question in questions:
            question_id = str(question.get('id', ''))
            analysis = analysis_map.get(question_id)
            
            if analysis:
                question_type = analysis.detected_type
                if question_type not in grouped:
                    grouped[question_type] = []
                grouped[question_type].append({
                    'question': question,
                    'analysis': {
                        'question_id': analysis.question_id,
                        'detected_type': analysis.detected_type,
                        'confidence': analysis.confidence,
                        'reasoning': analysis.reasoning,
                        'key_indicators': analysis.key_indicators
                    }
                })
        
        return grouped
    
    async def migrate_question_type(self, question_type: str, questions_data: List[Dict[str, Any]], part_data: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate một nhóm questions cùng question_type"""
        
        # Load rules cho question type này
        base_rules = self._load_base_migration_rules()
        type_rules = self._load_question_type_rules(question_type)
        
        system_prompt = f"""You are an expert in migrating IELTS data. Your task is to convert questions of type \'{{question_type}}\' from the old structure to the new structure.

BASE MIGRATION RULES:
{base_rules}

SPECIFIC RULES FOR \'{{question_type}}\':
{type_rules}

IMPORTANT: You must return the correct JSON object format as follows, no additional text and anything else:
{{
  "question_sets": [
    {{
      "id": 1,
      "part_id": "part_id",
      "user_created": "user_created",
      "date_created": "date_created",
      "user_updated": "user_updated", 
      "date_updated": "date_updated",
      "question_type": "\'{{question_type}}\'",
      "question_count": 2,
      "title": "Questions 1-2",
      "description": "instruction text",
      "content": "content with gaps or options",
      "option_title": null,
      "options": null,
      "allow_reuse": null,
      "max_selections": null,
      "sort": 1
    }}
  ],
  "questions": [
    {{
      "id": 1,
      "status": "published",
      "sort": 1,
      "user_created": "user_created",
      "date_created": "date_created",
      "user_updated": "user_updated",
      "date_updated": "date_updated",
      "title": null,
      "content": null,
      "locate": null,
      "order": 1,
      "explain": "explanation text",
      "description": null,
      "content_writing": null,
      "time_to_think": null,
      "listen_from": null,
      "instruction": null,
      "writing_graph_image": null,
      "writing_graph_description": null,
      "writing_graph_type": null,
      "audio_url": null,
      "time_limit": 30,
      "max_words": null,
      "min_words": null,
      "text": null,
      "locate_info": null,
      "quiz_id": 0,
      "part_id": null,
      "type": "",
      "gap_fill_in_blank": null,
      "single_choice_radio": null,
      "selection": null,
      "mutilple_choice": null,
      "selection_option": null,
      "question_set_id": 1,
      "question_type": "question_type_value",
      "correct_answer": null,
      "correct_answers": ["answer"],
      "options": null
    }}
  ]
}}

ONLY RETURN JSON OBJECT, NO ADDITIONAL TEXT AND ANYTHING ELSE."""

        human_prompt = """Convert the following questions of type {question_type} into question sets and questions:

PART DATA:
{part_data}

QUESTIONS DATA:
{questions_data}

Group questions of the same type consecutively into question sets and convert according to the defined rules."""

        # Tạo messages trực tiếp để tránh template variable conflicts
        from langchain_core.messages import SystemMessage, HumanMessage
        
        try:
            # Check if LLM is available
            if self.llm is None:
                logger.info(f"No LLM available, using fallback migrate for {question_type}")
                return self._fallback_migrate_question_type(question_type, questions_data, part_data)
            
            # Tạo content trực tiếp để tránh template variable conflicts
            part_json = json.dumps(part_data, ensure_ascii=False, indent=2)
            questions_json = json.dumps(questions_data, ensure_ascii=False, indent=2)
            
            # Tạo system message với nội dung đã format sẵn
            # system_prompt đã được format với base_rules và type_rules rồi, chỉ cần replace {{question_type}}
            system_content = system_prompt.replace('{{question_type}}', question_type)
            
            # Tạo human message với nội dung đã format sẵn
            human_content = human_prompt.format(
                question_type=question_type,
                part_data=part_json,
                questions_data=questions_json
            )
            
            # Invoke LLM trực tiếp với messages
            messages = [
                SystemMessage(content=system_content),
                HumanMessage(content=human_content)
            ]
            
            response = await self.llm.ainvoke(messages)
            response_content = response.content if hasattr(response, 'content') else str(response)
            
            # Clean response content
            cleaned_content = self._clean_json_response(response_content)
            
            try:
                migration_data = json.loads(cleaned_content)
                logger.info(f"AI successfully migrated {question_type} questions")
                return migration_data
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse migrate response for {question_type} as JSON: {e}")
                logger.debug(f"Raw response: {response_content[:500]}...")
                return self._fallback_migrate_question_type(question_type, questions_data, part_data)
                
        except Exception as e:
            logger.error(f"Error in migrate_question_type for {question_type}: {e}")
            return self._fallback_migrate_question_type(question_type, questions_data, part_data)
    
    def _fallback_migrate_question_type(self, question_type: str, questions_data: List[Dict[str, Any]], part_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback migration cho specific question type"""
        
        # Dispatch to specific fallback methods
        if question_type == "GAP_FILLING":
            return self._fallback_migrate_gap_filling(questions_data, part_data)
        elif question_type == "SINGLE_SELECTION":
            return self._fallback_migrate_single_selection(questions_data, part_data)
        elif question_type == "MATCHING":
            return self._fallback_migrate_matching(questions_data, part_data)
        elif question_type == "MULTIPLE_CHOICE_MANY":
            return self._fallback_migrate_multiple_choice_many(questions_data, part_data)
        elif question_type == "NOTE_COMPLETION":
            return self._fallback_migrate_note_completion(questions_data, part_data)
        elif question_type == "SINGLE_CHOICE":
            return self._fallback_migrate_single_choice(questions_data, part_data)
        else:
            # Generic fallback
            return self._fallback_migrate_generic(question_type, questions_data, part_data)
    
    def _fallback_migrate_gap_filling(self, questions_data: List[Dict[str, Any]], part_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback migration cho GAP_FILLING"""
        question_sets = []
        questions = []
        
        for i, item in enumerate(questions_data):
            question = item['question']
            analysis = item['analysis']
            
            # Extract gaps from gap_fill_in_blank
            gap_content = question.get('gap_fill_in_blank', '')
            gaps = re.findall(r'\{[^}]+\}', gap_content)
            
            # Create question set
            question_set = {
                "id": i + 1,
                "part_id": part_data.get('id'),
                "user_created": question.get('user_created'),
                "date_created": question.get('date_created'),
                "user_updated": question.get('user_updated'),
                "date_updated": question.get('date_updated'),
                "question_type": "GAP_FILLING",
                "question_count": len(gaps),
                "title": f"Questions {question.get('order', i+1)}-{question.get('order', i+1) + len(gaps) - 1}",
                "description": question.get('title', ''),
                "content": re.sub(r'\{[^}]+\}', '______', gap_content) if gap_content else '',
                "option_title": None,
                "options": None,
                "allow_reuse": None,
                "max_selections": None,
                "sort": i + 1
            }
            question_sets.append(question_set)
            
            # Create individual questions for each gap
            explanations = question.get('explain', '').split('<div><strong>Câu ') if question.get('explain') else ['']
            
            for j, gap in enumerate(gaps):
                # Extract answer from gap {[answer][number]}
                gap_match = re.search(r'\{[^}]+\}', gap)
                answer_raw = ""
                if gap_match:
                    answer_match = re.search(r'\[([^\]]+)\]', gap)
                    if answer_match:
                        answer_raw = answer_match.group(1)
                
                # Process multiple answers (e.g., "labour | labor" -> ["labour", "labor"])
                correct_answers = []
                if answer_raw:
                    if '|' in answer_raw:
                        # Split by | and clean up
                        answers = [ans.strip() for ans in answer_raw.split('|')]
                        correct_answers = [ans for ans in answers if ans]
                    else:
                        correct_answers = [answer_raw]
                
                question_item = {
                    "id": len(questions) + 1 if isinstance(questions, list) else 1,
                    "status": "published",
                    "sort": j + 1,
                    "user_created": question.get('user_created'),
                    "date_created": question.get('date_created'),
                    "user_updated": question.get('user_updated'),
                    "date_updated": question.get('date_updated'),
                    "title": None,
                    "content": None,
                    "locate": None,
                    "order": question.get('order', i+1) + j,
                    "explain": explanations[j+1] if j+1 < len(explanations) else '',
                    "description": None,
                    "content_writing": None,
                    "time_to_think": None,
                    "listen_from": None,
                    "instruction": None,
                    "writing_graph_image": None,
                    "writing_graph_description": None,
                    "writing_graph_type": None,
                    "audio_url": None,
                    "time_limit": 30,
                    "max_words": None,
                    "min_words": None,
                    "text": None,
                    "locate_info": None,
                    "quiz_id": 0,
                    "part_id": None,
                    "type": "",
                    "gap_fill_in_blank": None,
                    "single_choice_radio": None,
                    "selection": None,
                    "mutilple_choice": None,
                    "selection_option": None,
                    "question_set_id": question_set["id"],
                    "question_type": question.get('question_type', 'FILL_BLANK'),
                    "correct_answer": None,
                    "correct_answers": correct_answers,
                    "options": None
                }
                questions.append(question_item)
        
        return {
            "question_sets": question_sets,
            "questions": questions
        }
    
    def _fallback_migrate_single_selection(self, questions_data: List[Dict[str, Any]], part_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback migration cho SINGLE_SELECTION"""
        # Group consecutive questions with same selection_option
        grouped_questions = []
        current_group = []
        
        for item in questions_data:
            question = item['question']
            if not current_group:
                current_group.append(item)
            else:
                # Check if same selection options
                prev_options = current_group[0]['question'].get('selection_option', [])
                curr_options = question.get('selection_option', [])
                if prev_options == curr_options:
                    current_group.append(item)
                else:
                    grouped_questions.append(current_group)
                    current_group = [item]
        
        if current_group:
            grouped_questions.append(current_group)
        
        question_sets = []
        questions = []
        
        for group_idx, group in enumerate(grouped_questions):
            first_question = group[0]['question']
            
            # Create options from selection_option
            options = []
            selection_options = first_question.get('selection_option', [])
            for opt in selection_options:
                option_text = opt.get('option', '')
                if option_text == 'TRUE':
                    options.append({"text": "YES", "option": "TRUE"})
                elif option_text == 'FALSE':
                    options.append({"text": "NO", "option": "FALSE"})
                else:
                    options.append({"text": option_text, "option": option_text})
            
            # Create question set
            start_order = group[0]['question'].get('order', group_idx * 10 + 1)
            end_order = group[-1]['question'].get('order', start_order + len(group) - 1)
            
            question_set = {
                "id": group_idx + 1,
                "part_id": part_data.get('id'),
                "user_created": first_question.get('user_created'),
                "date_created": first_question.get('date_created'),
                "user_updated": first_question.get('user_updated'),
                "date_updated": first_question.get('date_updated'),
                "question_type": "SINGLE_SELECTION",
                "question_count": len(group),
                "title": f"Questions {start_order}-{end_order}",
                "description": first_question.get('description', ''),
                "content": "",
                "option_title": "",
                "options": options,
                "allow_reuse": False,
                "max_selections": 0,
                "sort": group_idx + 1
            }
            question_sets.append(question_set)
            
            # Create individual questions
            for q_idx, item in enumerate(group):
                question = item['question']
                selection = question.get('selection', [])
                correct_answer = selection[0].get('answer', '') if selection else ''
                question_text = selection[0].get('text', '') if selection else ''
                
                question_item = {
                    "id": len(questions) + 1,
                    "status": "published",
                    "sort": q_idx + 1,
                    "user_created": question.get('user_created'),
                    "date_created": question.get('date_created'),
                    "user_updated": question.get('user_updated'),
                    "date_updated": question.get('date_updated'),
                    "title": None,
                    "content": None,
                    "locate": None,
                    "order": question.get('order', start_order + q_idx),
                    "explain": question.get('explain', ''),
                    "description": None,
                    "content_writing": None,
                    "time_to_think": None,
                    "listen_from": None,
                    "instruction": None,
                    "writing_graph_image": None,
                    "writing_graph_description": None,
                    "writing_graph_type": None,
                    "audio_url": None,
                    "time_limit": 30,
                    "max_words": None,
                    "min_words": None,
                    "text": question_text,
                    "locate_info": None,
                    "quiz_id": 0,
                    "part_id": None,
                    "type": "",
                    "gap_fill_in_blank": None,
                    "single_choice_radio": None,
                    "selection": None,
                    "mutilple_choice": None,
                    "selection_option": None,
                    "question_set_id": question_set["id"],
                    "question_type": question.get('question_type', 'TRUE_FALSE'),
                    "correct_answer": correct_answer,
                    "correct_answers": None,
                    "options": None
                }
                questions.append(question_item)
        
        return {
            "question_sets": question_sets,
            "questions": questions
        }
    
    def _fallback_migrate_matching(self, questions_data: List[Dict[str, Any]], part_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback migration cho MATCHING"""
        # Group consecutive questions with same selection_option
        grouped_questions = []
        current_group = []
        
        for item in questions_data:
            question = item['question']
            if not current_group:
                current_group.append(item)
            else:
                # Check if same selection options (A-F, etc.)
                prev_options = current_group[0]['question'].get('selection_option', [])
                curr_options = question.get('selection_option', [])
                if prev_options == curr_options:
                    current_group.append(item)
                else:
                    grouped_questions.append(current_group)
                    current_group = [item]
        
        if current_group:
            grouped_questions.append(current_group)
        
        question_sets = []
        questions = []
        
        for group_idx, group in enumerate(grouped_questions):
            first_question = group[0]['question']
            
            # Create options from questions (text -> answer mapping)
            options = []
            for item in group:
                question = item['question']
                selection = question.get('selection', [])
                if selection:
                    question_text = selection[0].get('text', '')
                    answer = selection[0].get('answer', '')
                    options.append({"text": question_text, "option": answer})
            
            # Create question set
            start_order = group[0]['question'].get('order', group_idx * 10 + 1)
            end_order = group[-1]['question'].get('order', start_order + len(group) - 1)
            
            question_set = {
                "id": group_idx + 1,
                "part_id": part_data.get('id'),
                "user_created": first_question.get('user_created'),
                "date_created": first_question.get('date_created'),
                "user_updated": first_question.get('user_updated'),
                "date_updated": first_question.get('date_updated'),
                "question_type": "MATCHING",
                "question_count": len(group),
                "title": f"Questions {start_order}-{end_order}",
                "description": first_question.get('description', ''),
                "content": "",
                "option_title": "",
                "options": options,
                "allow_reuse": True,
                "max_selections": 0,
                "sort": group_idx + 1
            }
            question_sets.append(question_set)
            
            # Create individual questions
            for q_idx, item in enumerate(group):
                question = item['question']
                selection = question.get('selection', [])
                correct_answer = selection[0].get('answer', '') if selection else ''
                
                question_item = {
                    "id": len(questions) + 1,
                    "status": "published",
                    "sort": q_idx + 1,
                    "user_created": question.get('user_created'),
                    "date_created": question.get('date_created'),
                    "user_updated": question.get('user_updated'),
                    "date_updated": question.get('date_updated'),
                    "title": None,
                    "content": None,
                    "locate": None,
                    "order": question.get('order', start_order + q_idx),
                    "explain": question.get('explain', ''),
                    "description": None,
                    "content_writing": None,
                    "time_to_think": None,
                    "listen_from": None,
                    "instruction": None,
                    "writing_graph_image": None,
                    "writing_graph_description": None,
                    "writing_graph_type": None,
                    "audio_url": None,
                    "time_limit": 30,
                    "max_words": None,
                    "min_words": None,
                    "text": "",
                    "locate_info": None,
                    "quiz_id": 0,
                    "part_id": None,
                    "type": "",
                    "gap_fill_in_blank": None,
                    "single_choice_radio": None,
                    "selection": None,
                    "mutilple_choice": None,
                    "selection_option": None,
                    "question_set_id": question_set["id"],
                    "question_type": question.get('question_type', 'MATCHING_INFO'),
                    "correct_answer": correct_answer,
                    "correct_answers": None,
                    "options": None
                }
                questions.append(question_item)
        
        return {
            "question_sets": question_sets,
            "questions": questions
        }
    
    def _fallback_migrate_multiple_choice_many(self, questions_data: List[Dict[str, Any]], part_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback migration cho MULTIPLE_CHOICE_MANY"""
        question_sets = []
        questions = []
        
        for i, item in enumerate(questions_data):
            question = item['question']
            multiple_choice = question.get('mutilple_choice', [])
            
            # Create options từ multiple_choice
            options = []
            correct_answers = []
            for j, choice in enumerate(multiple_choice):
                letter = chr(ord('A') + j)  # A, B, C, D...
                options.append({
                    "text": choice.get('text', ''),
                    "option": letter
                })
                if choice.get('correct', False):
                    correct_answers.append(letter)
            
            # Determine max_selections từ description hoặc correct answers
            description = question.get('description', '')
            max_selections = len(correct_answers)
            if 'TWO' in description.upper():
                max_selections = 2
            elif 'THREE' in description.upper():
                max_selections = 3
            
            # Create question set
            question_set = {
                "id": i + 1,
                "part_id": part_data.get('id'),
                "user_created": question.get('user_created'),
                "date_created": question.get('date_created'),
                "user_updated": question.get('user_updated'),
                "date_updated": question.get('date_updated'),
                "question_type": "MULTIPLE_CHOICE_MANY",
                "question_count": 1,
                "title": f"Questions {question.get('order', i+1)}",
                "description": question.get('description', ''),
                "content": "",
                "option_title": "",
                "options": options,
                "allow_reuse": False,
                "max_selections": max_selections,
                "sort": i + 1
            }
            question_sets.append(question_set)
            
            # Create single question with multiple correct answers
            # Combine explanations từ correct options
            explanations = []
            for choice in multiple_choice:
                if choice.get('correct', False) and choice.get('explain'):
                    explanations.append(choice.get('explain'))
            
            combined_explanation = ' '.join(explanations) if explanations else question.get('explain', '')
            
            question_item = {
                "id": i + 1,
                "status": "published",
                "sort": 1,
                "user_created": question.get('user_created'),
                "date_created": question.get('date_created'),
                "user_updated": question.get('user_updated'),
                "date_updated": question.get('date_updated'),
                "title": question.get('title'),
                "content": None,
                "locate": None,
                "order": question.get('order', i + 1),
                "explain": combined_explanation,
                "description": None,
                "content_writing": None,
                "time_to_think": None,
                "listen_from": None,
                "instruction": None,
                "writing_graph_image": None,
                "writing_graph_description": None,
                "writing_graph_type": None,
                "audio_url": None,
                "time_limit": 30,
                "max_words": None,
                "min_words": None,
                "text": "",
                "locate_info": None,
                "quiz_id": 0,
                "part_id": None,
                "type": "",
                "gap_fill_in_blank": None,
                "single_choice_radio": None,
                "selection": None,
                "mutilple_choice": None,
                "selection_option": None,
                "question_set_id": question_set["id"],
                "question_type": "MULTIPLE",
                "correct_answer": None,
                "correct_answers": correct_answers,
                "options": None
            }
            questions.append(question_item)
        
        return {
            "question_sets": question_sets,
            "questions": questions
        }
    
    def _fallback_migrate_note_completion(self, questions_data: List[Dict[str, Any]], part_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback migration cho NOTE_COMPLETION"""
        question_sets = []
        questions = []
        
        for i, item in enumerate(questions_data):
            question = item['question']
            gap_content = question.get('gap_fill_in_blank', '')
            
            # Extract vocabulary list từ gap_content
            vocab_pattern = r'<h3>List of words</h3>(.*?)<h3>'
            vocab_match = re.search(vocab_pattern, gap_content, re.DOTALL)
            
            options = []
            if vocab_match:
                vocab_section = vocab_match.group(1)
                # Extract A, B, C... options
                option_pattern = r'<strong>([A-Z])</strong>\s*([^<]+)'
                option_matches = re.findall(option_pattern, vocab_section)
                for letter, word in option_matches:
                    options.append({
                        "text": word.strip(),
                        "option": letter
                    })
            
            # Remove vocabulary section from content
            content = re.sub(r'<h3>List of words</h3>.*?<h3>', '<h3>', gap_content, flags=re.DOTALL)
            # Convert gaps to ______
            content = re.sub(r'\{[^}]+\}', '______', content)
            
            # Extract gaps for question count
            gaps = re.findall(r'\{[^}]+\}', gap_content)
            
            # Create question set
            question_set = {
                "id": i + 1,
                "part_id": part_data.get('id'),
                "user_created": question.get('user_created'),
                "date_created": question.get('date_created'),
                "user_updated": question.get('user_updated'),
                "date_updated": question.get('date_updated'),
                "question_type": "NOTE_COMPLETION",
                "question_count": len(gaps),
                "title": f"Questions {question.get('order', i+1)}-{question.get('order', i+1) + len(gaps) - 1}",
                "description": question.get('title', ''),
                "content": content,
                "option_title": "",
                "options": options,
                "allow_reuse": True,
                "max_selections": 0,
                "sort": i + 1
            }
            question_sets.append(question_set)
            
            # Create individual questions for each gap
            explanations = question.get('explain', '').split('<div><strong>Câu ') if question.get('explain') else ['']
            
            for j, gap in enumerate(gaps):
                # Extract answer từ gap {[letter][number]}
                answer_match = re.search(r'\[([A-Z])\]', gap)
                answer = answer_match.group(1) if answer_match else ''
                
                question_item = {
                    "id": len(questions) + 1,
                    "status": "published",
                    "sort": j + 1,
                    "user_created": question.get('user_created'),
                    "date_created": question.get('date_created'),
                    "user_updated": question.get('user_updated'),
                    "date_updated": question.get('date_updated'),
                    "title": None,
                    "content": None,
                    "locate": None,
                    "order": question.get('order', i+1) + j,
                    "explain": explanations[j+1] if j+1 < len(explanations) else '',
                    "description": None,
                    "content_writing": None,
                    "time_to_think": None,
                    "listen_from": None,
                    "instruction": None,
                    "writing_graph_image": None,
                    "writing_graph_description": None,
                    "writing_graph_type": None,
                    "audio_url": None,
                    "time_limit": 30,
                    "max_words": None,
                    "min_words": None,
                    "text": "",
                    "locate_info": None,
                    "quiz_id": 0,
                    "part_id": None,
                    "type": "",
                    "gap_fill_in_blank": None,
                    "single_choice_radio": None,
                    "selection": None,
                    "mutilple_choice": None,
                    "selection_option": None,
                    "question_set_id": question_set["id"],
                    "question_type": "NOTE_COMPLETION",
                    "correct_answer": answer,
                    "correct_answers": None,
                    "options": None
                }
                questions.append(question_item)
        
        return {
            "question_sets": question_sets,
            "questions": questions
        }
    
    def _fallback_migrate_single_choice(self, questions_data: List[Dict[str, Any]], part_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback migration cho SINGLE_CHOICE"""
        # Group consecutive questions with same description pattern
        grouped_questions = []
        current_group = []
        
        for item in questions_data:
            question = item['question']
            if not current_group:
                current_group.append(item)
            else:
                # Check if same description pattern (Questions X-Y)
                prev_desc = current_group[0]['question'].get('description', '')
                curr_desc = question.get('description', '')
                if prev_desc == curr_desc or not curr_desc:
                    current_group.append(item)
                else:
                    grouped_questions.append(current_group)
                    current_group = [item]
        
        if current_group:
            grouped_questions.append(current_group)
        
        question_sets = []
        questions = []
        
        for group_idx, group in enumerate(grouped_questions):
            first_question = group[0]['question']
            
            # Create question set
            start_order = group[0]['question'].get('order', group_idx * 10 + 1)
            end_order = group[-1]['question'].get('order', start_order + len(group) - 1)
            
            question_set = {
                "id": group_idx + 1,
                "part_id": part_data.get('id'),
                "user_created": first_question.get('user_created'),
                "date_created": first_question.get('date_created'),
                "user_updated": first_question.get('user_updated'),
                "date_updated": first_question.get('date_updated'),
                "question_type": "SINGLE_CHOICE",
                "question_count": len(group),
                "title": f"Questions {start_order}-{end_order}",
                "description": first_question.get('description', ''),
                "content": "",
                "option_title": "",
                "options": None,  # Each question has its own options
                "allow_reuse": False,
                "max_selections": 0,
                "sort": group_idx + 1
            }
            question_sets.append(question_set)
            
            # Create individual questions
            for q_idx, item in enumerate(group):
                question = item['question']
                single_choice = question.get('single_choice_radio', [])
                
                # Create options for this question
                question_options = []
                correct_answer = ""
                for j, choice in enumerate(single_choice):
                    letter = chr(ord('A') + j)  # A, B, C, D...
                    question_options.append({
                        "text": choice.get('text', ''),
                        "option": letter,
                        "is_correct": choice.get('correct', False)
                    })
                    if choice.get('correct', False):
                        correct_answer = letter
                
                question_item = {
                    "id": len(questions) + 1,
                    "status": "published",
                    "sort": q_idx + 1,
                    "user_created": question.get('user_created'),
                    "date_created": question.get('date_created'),
                    "user_updated": question.get('user_updated'),
                    "date_updated": question.get('date_updated'),
                    "title": None,
                    "content": None,
                    "locate": None,
                    "order": question.get('order', start_order + q_idx),
                    "explain": question.get('explain', ''),
                    "description": None,
                    "content_writing": None,
                    "time_to_think": None,
                    "listen_from": None,
                    "instruction": None,
                    "writing_graph_image": None,
                    "writing_graph_description": None,
                    "writing_graph_type": None,
                    "audio_url": None,
                    "time_limit": 30,
                    "max_words": None,
                    "min_words": None,
                    "text": question.get('title', ''),
                    "locate_info": None,
                    "quiz_id": 0,
                    "part_id": None,
                    "type": "",
                    "gap_fill_in_blank": None,
                    "single_choice_radio": None,
                    "selection": None,
                    "mutilple_choice": None,
                    "selection_option": None,
                    "question_set_id": question_set["id"],
                    "question_type": "SINGLE-CHOICE",
                    "correct_answer": correct_answer,
                    "correct_answers": None,
                    "options": question_options
                }
                questions.append(question_item)
        
        return {
            "question_sets": question_sets,
            "questions": questions
        }
    
    def _fallback_migrate_generic(self, question_type: str, questions_data: List[Dict[str, Any]], part_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generic fallback migration cho các question type khác"""
        question_sets = []
        questions = []
        
        # Create a single question set for all questions
        if questions_data:
            first_question = questions_data[0]['question']
            
            question_set = {
                "id": 1,
                "part_id": part_data.get('id'),
                "user_created": first_question.get('user_created'),
                "date_created": first_question.get('date_created'),
                "user_updated": first_question.get('user_updated'),
                "date_updated": first_question.get('date_updated'),
                "question_type": question_type,
                "question_count": len(questions_data),
                "title": f"Questions 1-{len(questions_data)}",
                "description": first_question.get('title', '') or first_question.get('description', ''),
                "content": "",
                "option_title": None,
                "options": None,
                "allow_reuse": None,
                "max_selections": None,
                "sort": 1
            }
            question_sets.append(question_set)
            
            # Create individual questions
            for i, item in enumerate(questions_data):
                question = item['question']
                
                question_item = {
                    "id": i + 1,
                    "status": "published",
                    "sort": i + 1,
                    "user_created": question.get('user_created'),
                    "date_created": question.get('date_created'),
                    "user_updated": question.get('user_updated'),
                    "date_updated": question.get('date_updated'),
                    "title": question.get('title'),
                    "content": question.get('content'),
                    "locate": None,
                    "order": question.get('order', i + 1),
                    "explain": question.get('explain', ''),
                    "description": question.get('description'),
                    "content_writing": None,
                    "time_to_think": None,
                    "listen_from": None,
                    "instruction": None,
                    "writing_graph_image": None,
                    "writing_graph_description": None,
                    "writing_graph_type": None,
                    "audio_url": None,
                    "time_limit": 30,
                    "max_words": None,
                    "min_words": None,
                    "text": None,
                    "locate_info": None,
                    "quiz_id": 0,
                    "part_id": None,
                    "type": "",
                    "gap_fill_in_blank": None,
                    "single_choice_radio": None,
                    "selection": None,
                    "mutilple_choice": None,
                    "selection_option": None,
                    "question_set_id": question_set["id"],
                    "question_type": question.get('question_type', ''),
                    "correct_answer": None,
                    "correct_answers": None,
                    "options": None
                }
                questions.append(question_item)
        
        return {
            "question_sets": question_sets,
            "questions": questions
        }
    
    def _clean_json_response(self, response_content: str) -> str:
        """Clean AI response to extract JSON content"""
        # Remove markdown code blocks
        if "```json" in response_content:
            start = response_content.find("```json") + 7
            end = response_content.find("```", start)
            if end != -1:
                response_content = response_content[start:end].strip()
        elif "```" in response_content:
            start = response_content.find("```") + 3
            end = response_content.find("```", start)
            if end != -1:
                response_content = response_content[start:end].strip()
        
        # Remove leading/trailing whitespace and newlines
        response_content = response_content.strip()
        
        # Try to find JSON object/array bounds
        if response_content.startswith('[') and response_content.endswith(']'):
            return response_content
        elif response_content.startswith('{') and response_content.endswith('}'):
            return response_content
        else:
            # Try to extract JSON from text
            import re
            json_match = re.search(r'(\[.*\]|\{.*\})', response_content, re.DOTALL)
            if json_match:
                return json_match.group(1)
        
        return response_content
    
    async def transform_to_question_sets_by_type(self, part_data: Dict[str, Any], question_analyses: List[QuestionTypeAnalysis]) -> Dict[str, Any]:
        """
        AI Agent 2: Chuyển đổi thành question sets bằng cách migrate từng question type riêng biệt
        """
        try:
            # Group questions theo question type
            questions = part_data.get('questions', [])
            grouped_questions = self._group_questions_by_type(questions, question_analyses)
            
            logger.info(f"Grouped questions by types: {list(grouped_questions.keys())}")
            
            # Migrate từng question type riêng biệt
            all_question_sets = []
            all_questions = []
            
            question_set_id_counter = 1
            question_id_counter = 1
            
            for question_type, questions_data in grouped_questions.items():
                print("custom test --------------- (questions_data) --------------- ")
                logger.info(f"Migrating {len(questions_data)} questions of type {question_type}")
                
                # Migrate question type này
                type_result = await self.migrate_question_type(question_type, questions_data, part_data)
                
                # Update IDs để tránh conflict
                for qs in type_result.get('question_sets', []):
                    original_id = qs['id']
                    qs['id'] = question_set_id_counter
                    
                    # Update question_set_id trong questions tương ứng
                    for q in type_result.get('questions', []):
                        if q.get('question_set_id') == original_id:
                            q['question_set_id'] = question_set_id_counter
                    
                    question_set_id_counter += 1
                    all_question_sets.append(qs)
                
                for q in type_result.get('questions', []):
                    q['id'] = question_id_counter
                    question_id_counter += 1
                    all_questions.append(q)
            
            # Extract quiz và parts data từ part_data
            quiz_data = {
                key: value for key, value in part_data.items() 
                if key not in ['questions', 'parts']
            }
            
            # Set required fields cho quiz
            quiz_data['vote_count'] = 0
            quiz_data['total_submitted'] = 0
            
            # Create parts data với nested question_sets và questions
            parts_data = []
            if 'parts' in part_data:
                for part in part_data['parts']:
                    part_copy = part.copy()
                    # Remove gaps from content
                    if 'content' in part_copy and part_copy['content']:
                        content = part_copy['content']
                        # Remove gaps pattern {[answer][number]}
                        content = re.sub(r'\{[^}]+\}', '', content)
                        part_copy['content'] = content
                    
                    # Set file_id từ quiz.listening nếu có
                    if 'listening' in quiz_data and quiz_data['listening']:
                        part_copy['file_id'] = quiz_data['listening']
                    
                    # Thêm question_sets vào part (nested structure)
                    part_question_sets = []
                    for qs in all_question_sets:
                        if qs.get('part_id') == part_copy.get('id'):
                            qs_copy = qs.copy()
                            # Thêm questions vào question_set (nested structure)
                            qs_questions = []
                            for q in all_questions:
                                if q.get('question_set_id') == qs_copy.get('id'):
                                    qs_questions.append(q)
                            qs_copy['questions'] = qs_questions
                            part_question_sets.append(qs_copy)
                    
                    part_copy['question_sets'] = part_question_sets
                    parts_data.append(part_copy)
            else:
                # Nếu không có parts trong part_data, tạo từ quiz data
                part_data_single = {
                    "id": part_data.get('id', 1),
                    "sort": 1,
                    "user_created": part_data.get('user_created'),
                    "date_created": part_data.get('date_created'),
                    "date_updated": part_data.get('date_updated'),
                    "title": part_data.get('title', 'Part 1'),
                    "order": None,
                    "content": part_data.get('content', ''),
                    "quiz": quiz_data.get('id'),
                    "time": None,
                    "passage": 1,
                    "simplified_content": None,
                    "question_count": 0,
                    "listen_from": None,
                    "listen_to": None,
                    "instruction": None,
                    "task_instruction": None,
                    "transcription": None,
                    "file_id": quiz_data.get('listening')
                }
                
                # Thêm question_sets vào part (nested structure)
                part_question_sets = []
                for qs in all_question_sets:
                    qs_copy = qs.copy()
                    # Thêm questions vào question_set (nested structure)
                    qs_questions = []
                    for q in all_questions:
                        if q.get('question_set_id') == qs_copy.get('id'):
                            qs_questions.append(q)
                    qs_copy['questions'] = qs_questions
                    part_question_sets.append(qs_copy)
                
                part_data_single['question_sets'] = part_question_sets
                parts_data = [part_data_single]
            
            # Thêm parts vào quiz (nested structure)
            quiz_data['parts'] = parts_data
            
            migration_result = {
                "quiz": quiz_data
            }
            
            print("custom test --------------- (all_question_sets) --------------- ")
            print("custom test --------------- (all_questions) --------------- ")
            logger.info(f"Successfully migrated to {len(all_question_sets)} question sets and {len(all_questions)} questions")
            return migration_result
            
        except Exception as e:
            logger.error(f"Error in transform_to_question_sets_by_type: {e}")
            # Fallback to old method if available
            return self._fallback_transform_by_type(part_data, question_analyses)
    
    def _fallback_transform_by_type(self, part_data: Dict[str, Any], question_analyses: List[QuestionTypeAnalysis]) -> Dict[str, Any]:
        """Fallback transformation khi AI không hoạt động"""
        try:
            questions = part_data.get('questions', [])
            grouped_questions = self._group_questions_by_type(questions, question_analyses)
            
            all_question_sets = []
            all_questions = []
            
            question_set_id_counter = 1
            question_id_counter = 1
            
            for question_type, questions_data in grouped_questions.items():
                type_result = self._fallback_migrate_question_type(question_type, questions_data, part_data)
                
                # Update IDs
                for qs in type_result.get('question_sets', []):
                    original_id = qs['id']
                    qs['id'] = question_set_id_counter
                    
                    # Update question_set_id trong questions
                    for q in type_result.get('questions', []):
                        if q.get('question_set_id') == original_id:
                            q['question_set_id'] = question_set_id_counter
                    
                    question_set_id_counter += 1
                    all_question_sets.append(qs)
                
                for q in type_result.get('questions', []):
                    q['id'] = question_id_counter
                    question_id_counter += 1
                    all_questions.append(q)
            
            # Create result structure với nested format
            quiz_data = {key: value for key, value in part_data.items() if key not in ['questions', 'parts']}
            quiz_data['vote_count'] = 0
            quiz_data['total_submitted'] = 0
            
            parts_data = part_data.get('parts', [])
            if not parts_data:
                parts_data = [{
                    "id": part_data.get('id', 1),
                    "sort": 1,
                    "user_created": part_data.get('user_created'),
                    "date_created": part_data.get('date_created'),
                    "date_updated": part_data.get('date_updated'),
                    "title": part_data.get('title', 'Part 1'),
                    "content": part_data.get('content', ''),
                    "quiz": quiz_data.get('id'),
                    "passage": 1,
                    "file_id": quiz_data.get('listening')
                }]
            
            # Thêm question_sets vào parts (nested structure)
            for part in parts_data:
                part_question_sets = []
                for qs in all_question_sets:
                    if qs.get('part_id') == part.get('id'):
                        qs_copy = qs.copy()
                        # Thêm questions vào question_set (nested structure)
                        qs_questions = []
                        for q in all_questions:
                            if q.get('question_set_id') == qs_copy.get('id'):
                                qs_questions.append(q)
                        qs_copy['questions'] = qs_questions
                        part_question_sets.append(qs_copy)
                
                part['question_sets'] = part_question_sets
            
            # Thêm parts vào quiz (nested structure)
            quiz_data['parts'] = parts_data
            
            return {
                "quiz": quiz_data
            }
            
        except Exception as e:
            logger.error(f"Error in fallback transform by type: {e}")
            return {
                "quiz": {
                    "parts": []
                }
            }
    
    async def analyze_question_types(self, questions: List[Dict[str, Any]]) -> List[QuestionTypeAnalysis]:
        """
        AI Agent 1: Phân tích loại câu hỏi
        """
        try:
            # Check if LLM is available
            if self.llm is None:
                logger.info("No LLM available, using fallback analysis")
                return self._fallback_question_analysis(questions)
            
            # Use AI analysis if available
            system_prompt = """You are an expert in analyzing IELTS question types. Your task is to identify the question type for each question based on its structure and content.

QUESTION TYPES:
- GAP_FILLING: Questions with gaps to fill, usually has gap_fill_in_blank field
- SINGLE_SELECTION: True/False/Not Given questions, usually has selection and selection_option fields
- MATCHING: Matching information questions, usually has selection with paragraph letters
- MULTIPLE_CHOICE_MANY: Multiple choice with multiple correct answers, has mutilple_choice field
- NOTE_COMPLETION: Note completion with word list, has gap_fill_in_blank with vocabulary list
- SINGLE_CHOICE: Single choice questions, has single_choice_radio field

Return JSON array of analysis objects."""

            human_prompt = """Analyze the following questions and identify their types:

{questions}

Return analysis for each question with question_id, detected_type, confidence, reasoning, and key_indicators."""

            questions_json = json.dumps(questions, ensure_ascii=False, indent=2)
            
            # This would be AI analysis - for now use fallback
            return self._fallback_question_analysis(questions)
            
        except Exception as e:
            logger.error(f"Error in analyze_question_types: {e}")
            return self._fallback_question_analysis(questions)
    
    def _fallback_question_analysis(self, questions: List[Dict[str, Any]]) -> List[QuestionTypeAnalysis]:
        """Fallback analysis khi AI không hoạt động"""
        analyses = []
        
        for question in questions:
            question_id = str(question.get('id', ''))
            detected_type = self._simple_type_detection(question)
            
            analysis = QuestionTypeAnalysis(
                question_id=question_id,
                detected_type=detected_type,
                confidence=0.8,
                reasoning=f"Detected based on question structure and fields",
                key_indicators=[f"type: {question.get('type')}", f"question_type: {question.get('question_type')}"]
            )
            analyses.append(analysis)
        
        return analyses
    
    def _simple_type_detection(self, question: Dict[str, Any]) -> str:
        """Simple rule-based question type detection"""
        
        # Check for GAP_FILLING
        if question.get('gap_fill_in_blank') and question.get('type') == 'FILL-IN-THE-BLANK':
            # Check if it has vocabulary list (NOTE_COMPLETION)
            gap_content = question.get('gap_fill_in_blank', '')
            if 'List of words' in gap_content or '<strong>A</strong>' in gap_content:
                return 'NOTE_COMPLETION'
            else:
                return 'GAP_FILLING'
        
        # Check for SINGLE_SELECTION (True/False/Not Given)
        if question.get('type') == 'SINGLE-SELECTION' and question.get('selection_option'):
            options = question.get('selection_option', [])
            option_values = [opt.get('option', '') for opt in options]
            if 'TRUE' in option_values and 'FALSE' in option_values:
                return 'SINGLE_SELECTION'
            elif question.get('question_type') == 'MATCHING_INFO':
                return 'MATCHING'
            else:
                return 'SINGLE_SELECTION'
        
        # Check for MULTIPLE_CHOICE_MANY
        if question.get('type') == 'MULTIPLE' and question.get('mutilple_choice'):
            return 'MULTIPLE_CHOICE_MANY'
        
        # Check for SINGLE_CHOICE
        if question.get('type') == 'SINGLE-RADIO' and question.get('single_choice_radio'):
            return 'SINGLE_CHOICE'
        
        # Check for MATCHING based on question_type
        if question.get('question_type') == 'MATCHING_INFO':
            return 'MATCHING'
        
        # Default fallback
        question_type = question.get('question_type', '')
        if 'FILL' in question_type.upper():
            return 'GAP_FILLING'
        elif 'TRUE_FALSE' in question_type.upper():
            return 'SINGLE_SELECTION'
        elif 'MATCHING' in question_type.upper():
            return 'MATCHING'
        elif 'MULTIPLE' in question_type.upper():
            return 'MULTIPLE_CHOICE_MANY'
        else:
            return 'GAP_FILLING'  # Default fallback 