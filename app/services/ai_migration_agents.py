import logging
import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime

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

class QuestionSetStructure(BaseModel):
    """Cấu trúc question set"""
    type: str = Field(description="Loại question set")
    title: str = Field(description="Tiêu đề")
    content: str = Field(description="Nội dung chính")
    instructions: str = Field(description="Hướng dẫn")
    questions: List[Dict[str, Any]] = Field(description="Danh sách câu hỏi")
    options: List[Dict[str, str]] = Field(description="Các lựa chọn")
    metadata: Dict[str, Any] = Field(description="Metadata bổ sung")

class PartStructure(BaseModel):
    """Cấu trúc part"""
    title: str = Field(description="Tiêu đề part")
    description: str = Field(description="Mô tả part")
    content: str = Field(description="Nội dung passage")
    question_sets: List[QuestionSetStructure] = Field(description="Danh sách question sets")
    order: int = Field(description="Thứ tự part")

class MigrationResult(BaseModel):
    """Kết quả migration"""
    quiz_title: str = Field(description="Tiêu đề quiz")
    quiz_type: str = Field(description="Loại quiz")
    parts: List[PartStructure] = Field(description="Danh sách parts")
    metadata: Dict[str, Any] = Field(description="Metadata")

class AIMigrationAgents:
    """AI Agents cho migration workflow với multi-provider support"""
    
    def __init__(self, 
                 openrouter_api_key: str = None,
                 gpt_api_key: str = None, 
                 gemini_api_key: str = None,
                 claude_api_key: str = None,
                 provider: str = "openai",
                 model: str = "gpt-4o-mini"):
        
        self.provider = provider
        self.model = model
        
        # Setup LLM based on available keys
        self.llm = self._setup_llm(
            openrouter_api_key=openrouter_api_key,
            gpt_api_key=gpt_api_key,
            gemini_api_key=gemini_api_key,
            claude_api_key=claude_api_key
        )
        
        # Load structure rules
        self.structure_rules = self._load_structure_rules()
        
    def _setup_llm(self, openrouter_api_key=None, gpt_api_key=None, gemini_api_key=None, claude_api_key=None):
        """Setup LLM dựa trên API keys có sẵn"""
        
        # Thử OpenRouter trước (thường có nhiều models)
        if openrouter_api_key:
            try:
                from langchain_openai import ChatOpenAI
                logger.info("Using OpenRouter API")
                return ChatOpenAI(
                    api_key=openrouter_api_key,
                    base_url="https://openrouter.ai/api/v1",
                    model="openai/gpt-4o-mini",  # hoặc model khác trên OpenRouter
                    temperature=DEFAULT_TEMPERATURE,
                    max_tokens=DEFAULT_MAX_TOKENS,
                    request_timeout=30  # 30 seconds timeout
                )
            except Exception as e:
                logger.warning(f"Failed to setup OpenRouter: {e}")
        
        # Thử GPT API
        if gpt_api_key:
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
        if gemini_api_key:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                logger.info("Using Google Gemini API")
                return ChatGoogleGenerativeAI(
                    google_api_key=gemini_api_key,
                    model="gemini-1.5-flash",
                    temperature=DEFAULT_TEMPERATURE,
                    max_output_tokens=DEFAULT_MAX_TOKENS
                )
            except Exception as e:
                logger.warning(f"Failed to setup Gemini: {e}")
        
        # Thử Claude API
        if claude_api_key:
            try:
                from langchain_anthropic import ChatAnthropic
                logger.info("Using Anthropic Claude API")
                return ChatAnthropic(
                    anthropic_api_key=claude_api_key,
                    model="claude-3-haiku-20240307",
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
        """Load quy tắc chuyển đổi từ file"""
        try:
            with open("import-data-tool/prompt/structure-rules.md", "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.warning(f"Could not load structure rules: {e}")
            return ""
    
    async def analyze_question_types(self, questions: List[Dict[str, Any]]) -> List[QuestionTypeAnalysis]:
        """
        AI Agent 1: Phân tích loại câu hỏi
        """
        system_prompt = """Bạn là chuyên gia phân tích câu hỏi IELTS. Nhiệm vụ của bạn là phân tích và xác định chính xác loại câu hỏi dựa trên cấu trúc dữ liệu.

QUYỀN TẮC PHÂN LOẠI:
{structure_rules}

QUAN TRỌNG: Bạn PHẢI trả về CHÍNH XÁC JSON array format như sau, không có text thêm:
[
  {{
    "question_id": "string",
    "detected_type": "GAP_FILLING|SINGLE_SELECTION|MATCHING|MULTIPLE_CHOICE_MANY|NOTE_COMPLETION|SINGLE_CHOICE",
    "confidence": 0.9,
    "reasoning": "string",
    "key_indicators": ["string1", "string2"]
  }}
]

Lưu ý:
- Phân tích kỹ các trường type, question_type, gap_fill_in_blank, selection, mutilple_choice, single_choice_radio
- Chú ý đặc biệt đến NOTE_COMPLETION (có bảng từ vựng "List of words")
- TRUE_FALSE thường có options ["TRUE", "FALSE", "NOT GIVEN"] hoặc ["YES", "NO", "NOT GIVEN"]

CHỈ TRẢ VỀ JSON ARRAY, KHÔNG CÓ TEXT KHÁC."""

        human_prompt = """Phân tích các câu hỏi sau và trả về JSON array:

{questions_data}"""

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(human_prompt)
        ])
        
        try:
            # Check if LLM is available
            if self.llm is None:
                logger.info("No LLM available, using fallback analysis")
                return self._fallback_question_analysis(questions)
            
            questions_json = json.dumps(questions, ensure_ascii=False, indent=2)
            
            # Tạo chain
            chain = prompt | self.llm
            
            # Invoke với parameters
            response = await chain.ainvoke({
                "structure_rules": self.structure_rules,
                "questions_data": questions_json
            })
            
            # Parse response
            response_content = response.content if hasattr(response, 'content') else str(response)
            
            # Clean response content - remove markdown code blocks if present
            cleaned_content = self._clean_json_response(response_content)
            
            try:
                # Thử parse JSON trực tiếp
                analyses_data = json.loads(cleaned_content)
                
                # Convert to Pydantic objects
                result = []
                for analysis in analyses_data:
                    result.append(QuestionTypeAnalysis(**analysis))
                
                logger.info(f"AI successfully analyzed {len(result)} questions")
                return result
                
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse AI response as JSON: {e}")
                logger.debug(f"Raw response: {response_content[:500]}...")
                return self._fallback_question_analysis(questions)
                
        except Exception as e:
            logger.error(f"Error in analyze_question_types: {e}")
            # Fallback to simple analysis
            return self._fallback_question_analysis(questions)
    
    async def transform_to_question_sets(self, part_data: Dict[str, Any], question_analyses: List[QuestionTypeAnalysis]) -> List[QuestionSetStructure]:
        """
        AI Agent 2: Chuyển đổi thành question sets
        """
        system_prompt = """Bạn là chuyên gia chuyển đổi dữ liệu IELTS. Nhiệm vụ của bạn là chuyển đổi dữ liệu từ cấu trúc cũ sang cấu trúc mới theo các quy tắc đã định nghĩa.

QUYỀN TẮC CHUYỂN ĐỔI:
{structure_rules}

QUAN TRỌNG: Bạn PHẢI trả về CHÍNH XÁC JSON array format như sau, không có text thêm:
[
  {{
    "type": "GAP_FILLING",
    "title": "Questions 1-7",
    "content": "Complete the notes below...",
    "instructions": "Choose ONE WORD ONLY...",
    "questions": [
      {{"content": "Gap 1", "order": 1}},
      {{"content": "Gap 2", "order": 2}}
    ],
    "options": [],
    "metadata": {{"source": "gap_fill_in_blank"}}
  }}
]

Các nguyên tắc chuyển đổi:

1. GAP_FILLING:
   - Chuyển {{[answer][number]}} thành ______
   - Tạo riêng question cho mỗi gap
   - Content chứa text với gaps

2. SINGLE_SELECTION (TRUE/FALSE):
   - Options cố định: ["TRUE", "FALSE", "NOT GIVEN"] hoặc ["YES", "NO", "NOT GIVEN"]
   - Questions từ selection data
   - Content từ title + description

3. MATCHING:
   - Options từ selection_option
   - Questions từ selection text
   - allow_reuse = true

4. MULTIPLE_CHOICE_MANY:
   - Options từ mutilple_choice
   - max_selections = số đáp án đúng
   - Questions thường chỉ có 1

5. NOTE_COMPLETION:
   - Tách "List of words" thành options
   - Chuyển {{[letter][number]}} thành <span class="gap-placeholder">
   - Content không chứa bảng từ vựng

6. SINGLE_CHOICE:
   - Options từ single_choice_radio
   - Mỗi question có options riêng

CHỈ TRẢ VỀ JSON ARRAY, KHÔNG CÓ TEXT KHÁC."""

        human_prompt = """Chuyển đổi part data sau thành question sets:

PART DATA:
{part_data}

QUESTION ANALYSES:
{question_analyses}

Hãy nhóm các câu hỏi cùng loại liên tiếp thành question sets và chuyển đổi theo đúng quy tắc."""

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(human_prompt)
        ])
        
        try:
            # Check if LLM is available
            if self.llm is None:
                logger.info("No LLM available, using fallback transform")
                return self._fallback_question_sets(part_data, question_analyses)
            
            part_json = json.dumps(part_data, ensure_ascii=False, indent=2)
            analyses_json = json.dumps([analysis.dict() for analysis in question_analyses], ensure_ascii=False, indent=2)
            
            chain = prompt | self.llm
            
            response = await chain.ainvoke({
                "structure_rules": self.structure_rules,
                "part_data": part_json,
                "question_analyses": analyses_json
            })
            
            response_content = response.content if hasattr(response, 'content') else str(response)
            
            # Clean response content
            cleaned_content = self._clean_json_response(response_content)
            
            try:
                question_sets_data = json.loads(cleaned_content)
                
                result = []
                for qs_data in question_sets_data:
                    result.append(QuestionSetStructure(**qs_data))
                
                logger.info(f"AI successfully transformed {len(result)} question sets")
                return result
                
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse transform response as JSON: {e}")
                logger.debug(f"Raw response: {response_content[:500]}...")
                return self._fallback_question_sets(part_data, question_analyses)
                
        except Exception as e:
            logger.error(f"Error in transform_to_question_sets: {e}")
            return self._fallback_question_sets(part_data, question_analyses)
    
    async def validate_and_enhance(self, migration_result: Dict[str, Any]) -> MigrationResult:
        """
        AI Agent 3: Validation và enhancement
        """
        system_prompt = """Bạn là chuyên gia kiểm tra chất lượng dữ liệu IELTS. Nhiệm vụ của bạn là kiểm tra và cải thiện kết quả migration.

QUAN TRỌNG: Bạn PHẢI trả về CHÍNH XÁC JSON object format như sau, không có text thêm:
{{
  "quiz_title": "string",
  "quiz_type": "reading",
  "parts": [
    {{
      "title": "Part 1",
      "description": "string",
      "content": "passage content",
      "question_sets": [
        {{
          "type": "GAP_FILLING",
          "title": "Questions 1-7",
          "content": "content with gaps",
          "instructions": "instructions",
          "questions": [{{"content": "question", "order": 1}}],
          "options": [],
          "metadata": {{}}
        }}
      ],
      "order": 1
    }}
  ],
  "metadata": {{"validation_status": "completed"}}
}}

Kiểm tra các điểm sau:
1. Cấu trúc dữ liệu đúng format
2. Tất cả trường bắt buộc đều có
3. Content không bị thiếu hoặc lỗi
4. Options đầy đủ và đúng format
5. Questions có order đúng
6. HTML tags hợp lệ
7. Gap placeholders đúng format

CHỈ TRẢ VỀ JSON OBJECT, KHÔNG CÓ TEXT KHÁC."""

        human_prompt = """Kiểm tra và cải thiện migration result sau:

{migration_data}"""

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(human_prompt)
        ])
        
        try:
            # Check if LLM is available
            if self.llm is None:
                logger.info("No LLM available, using fallback validation")
                return self._fallback_validation(migration_result)
            
            migration_json = json.dumps(migration_result, ensure_ascii=False, indent=2)
            
            chain = prompt | self.llm
            
            response = await chain.ainvoke({
                "migration_data": migration_json
            })
            
            response_content = response.content if hasattr(response, 'content') else str(response)
            
            # Clean response content
            cleaned_content = self._clean_json_response(response_content)
            
            try:
                result_data = json.loads(cleaned_content)
                logger.info("AI validation completed successfully")
                return MigrationResult(**result_data)
                
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse validation response as JSON: {e}")
                logger.debug(f"Raw response: {response_content[:500]}...")
                return self._fallback_validation(migration_result)
                
        except Exception as e:
            logger.error(f"Error in validate_and_enhance: {e}")
            return self._fallback_validation(migration_result)
    
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
    
    def _fallback_question_analysis(self, questions: List[Dict[str, Any]]) -> List[QuestionTypeAnalysis]:
        """Fallback analysis khi AI không hoạt động"""
        results = []
        for i, question in enumerate(questions):
            q_type = self._simple_type_detection(question)
            results.append(QuestionTypeAnalysis(
                question_id=str(question.get("id", i)),
                detected_type=q_type,
                confidence=0.7,
                reasoning=f"Fallback detection based on type={question.get('type')} and question_type={question.get('question_type')}",
                key_indicators=[question.get("type", ""), question.get("question_type", "")]
            ))
        return results
    
    def _simple_type_detection(self, question: Dict[str, Any]) -> str:
        """Simple rule-based type detection"""
        q_type = question.get("type", "")
        question_type = question.get("question_type", "")
        
        if q_type == "FILL-IN-THE-BLANK" and question_type == "FILL_BLANK":
            gap_content = question.get("gap_fill_in_blank", "")
            if "List of words" in gap_content:
                return "NOTE_COMPLETION"
            return "GAP_FILLING"
        elif q_type == "SINGLE-SELECTION" and question_type == "TRUE_FALSE":
            return "SINGLE_SELECTION"
        elif q_type == "SINGLE-SELECTION" and question_type == "MATCHING_INFO":
            return "MATCHING"
        elif q_type == "MULTIPLE" and question_type == "MULTIPLE_CHOICE_MANY":
            return "MULTIPLE_CHOICE_MANY"
        elif q_type == "SINGLE-RADIO" and question_type == "MULTIPLE_CHOICE_ONE":
            return "SINGLE_CHOICE"
        else:
            return "GAP_FILLING"  # Default
    
    def _fallback_question_sets(self, part_data: Dict[str, Any], question_analyses: List[QuestionTypeAnalysis]) -> List[QuestionSetStructure]:
        """Fallback question sets creation"""
        question_sets = []
        questions = part_data.get("questions", [])
        
        # Group by type
        type_groups = {}
        for i, analysis in enumerate(question_analyses):
            q_type = analysis.detected_type
            if q_type not in type_groups:
                type_groups[q_type] = []
            if i < len(questions):
                type_groups[q_type].append(questions[i])
        
        # Create question sets
        for order, (q_type, qs) in enumerate(type_groups.items(), 1):
            question_set = QuestionSetStructure(
                type=q_type,
                title=f"Questions {order}",
                content="",
                instructions="",
                questions=[{"content": q.get("title", ""), "order": i+1} for i, q in enumerate(qs)],
                options=[],
                metadata={"fallback": True}
            )
            question_sets.append(question_set)
        
        return question_sets
    
    def _fallback_validation(self, migration_result: Dict[str, Any]) -> MigrationResult:
        """Fallback validation"""
        # Extract parts from migration_result if available
        parts = []
        if "parts" in migration_result:
            for part_data in migration_result["parts"]:
                part_structure = PartStructure(
                    title=part_data.get("title", "Part"),
                    description=part_data.get("description", ""),
                    content=part_data.get("content", ""),
                    question_sets=part_data.get("question_sets", []),
                    order=part_data.get("order", 1)
                )
                parts.append(part_structure)
        
        return MigrationResult(
            quiz_title=migration_result.get("quiz_title", "Untitled Quiz"),
            quiz_type=migration_result.get("quiz_type", "reading"),
            parts=parts,
            metadata={"fallback": True, "validation_errors": ["AI validation failed"]}
        ) 