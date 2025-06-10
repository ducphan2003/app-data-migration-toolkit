# Import Data Plan Using AI

## Overview
Hệ thống import data sử dụng AI (LangChain + LangGraph) để chuyển đổi bài thi IELTS thành cấu trúc database có thể xử lý.

## Input Format
### 1. Markdown/Word Format
User cần chuẩn bị nội dung theo format sau:
```markdown
# [Reading/Listening] Passage
## Passage Content
[content]
{image:image_id} <!-- Đánh dấu hình ảnh -->

## Questions 1-5
### Instructions
[instruction text]

### Questions
1. [question text] {type:gap} <!-- Đánh dấu gap filling -->
2. [question text] {type:choice} <!-- Đánh dấu multiple choice -->
   - Option A
   - Option B
   - Option C
3. [question text] {type:matching} <!-- Đánh dấu matching -->
   Source:
   - A. [text]
   - B. [text]
   Target:
   - 1. [text]
   - 2. [text]
```

### 2. Metadata
```yaml
type: reading/listening
audio_id: abc123 # cho listening
images: 
  - id: img1
    description: "diagram of..."
question_type: MULTIPLE_CHOICE_ONE/GAP_FILLING/etc
```

## Processing Flow

1. **Content Parsing**
   - Sử dụng LangChain để parse markdown/word thành structured data
   - Nhận diện các markers đặc biệt (images, gaps, choices)
   - Extract questions và answers

2. **Content Analysis**
   - AI phân tích nội dung để:
     - Xác định loại câu hỏi chính xác
     - Tách instructions và content
     - Group các câu hỏi liên quan
     - Validate cấu trúc dữ liệu

3. **Data Transformation**
   - Chuyển đổi thành cấu trúc database:
     - Tạo question_set record
     - Tạo questions với correct answers
     - Map relationships giữa các entities

4. **Output Generation**
   - Tạo SQL INSERT statements hoặc
   - Tạo SQLAlchemy ORM objects
   - Generate validation report

## AI Components

1. **Content Parser**
```python
class ContentParser:
    def parse_markdown(content: str) -> Dict:
        """
        Convert markdown/word document into AI-ready structured format
        
        Process Flow:
        1. Initial Parsing (Text -> Basic Structure)
           - Convert markdown/word to normalized format
           - Extract basic structure (headers, paragraphs, lists)
           - Preserve formatting and relationships
           Input: Raw markdown/word content
           Output: Normalized document structure
           Libraries: python-markdown, pypandoc
        
        2. Marker Processing (Basic Structure -> Tagged Structure)
           - Identify special markers ({type:gap}, {image:id})
           - Extract and validate markers
           - Group related markers
           Input: Normalized document
           Output: Document with processed markers
           Libraries: regex, parse
        
        3. Content Structuring (Tagged Structure -> Logical Structure)
           - Split into logical sections (passage, questions, etc)
           - Group related content
           - Build relationships between sections
           Input: Document with markers
           Output: Logically structured content
           Libraries: langchain.text_splitter
        
        4. AI-Ready Format (Logical Structure -> AI Structure)
           - Convert to format optimal for AI processing
           - Add metadata and context
           - Validate structure completeness
           Input: Logical structure
           Output: AI-ready dictionary structure
           Libraries: pydantic
        
        Example Output Structure:
        {
            "metadata": {
                "type": "reading/listening",
                "audio_id": "abc123",
                "images": [{"id": "img1", "desc": "..."}]
            },
            "content": {
                "passage": {
                    "text": "...",
                    "images": [...],
                    "sections": [...]
                },
                "questions": [
                    {
                        "type": "gap_filling",
                        "text": "...",
                        "markers": [...],
                        "context": "..."
                    }
                ]
            }
        }
        """
        pass
```

2. **Question Analyzer**
```python
class QuestionAnalyzer:
    def analyze_questions(parsed_content: Dict) -> List[Question]:
        # Use AI to analyze and structure questions
        # Return list of Question objects

        # Libraries & Techniques:
        # 1. LLM Integration:
        #    - langchain.chat_models: GPT-4/Claude for analysis
        #    - langchain.prompts: Structured prompting
        #    - langchain.output_parsers: Structure outputs
        #    - instructor: Pydantic-based structured outputs
        
        # 2. Question Classification:
        #    - sklearn: Traditional ML classification
        #    - spacy: NLP analysis and entity recognition
        #    - transformers: BERT/RoBERTa for classification
        #    - sentence-transformers: Semantic similarity
        
        # 3. Graph Processing:
        #    - langgraph: Build processing workflows
        #    - networkx: Analyze question relationships
        #    - rdflib: Knowledge graph representation
```

3. **Data Transformer**
```python
class DataTransformer:
    def to_database_format(analyzed_data: Dict) -> Union[str, OrmObjects]:
        # Convert to database format
        # Return SQL or ORM objects

        # Libraries & Techniques:
        # 1. ORM & Database:
        #    - SQLAlchemy: Python SQL toolkit and ORM
        #    - pydantic: Data validation and settings
        #    - marshmallow: Object serialization/deserialization
        #    - dataclasses: Structured data classes
        
        # 2. Data Validation:
        #    - jsonschema: Validate JSON structures
        #    - cerberus: Lightweight data validation
        #    - voluptuous: Data validation library
        
        # 3. Template Generation:
        #    - jinja2: Template engine for SQL
        #    - mako: Template library for Python
        #    - sqlalchemy-utils: Additional SQLAlchemy tools
```

## Validation & Quality Control

1. **Input Validation**
   - Check required markers và format
   - Validate image/audio references
   - Ensure question type compatibility

2. **Content Validation**
   - Verify question completeness
   - Check answer validity
   - Ensure logical grouping

3. **Output Validation**
   - Verify database constraints
   - Check relationships
   - Validate data integrity

## Error Handling

1. **User Errors**
   - Invalid format
   - Missing required fields
   - Incompatible question types

2. **Processing Errors**
   - AI parsing failures
   - Ambiguous content
   - Structural issues

3. **System Errors**
   - Database constraints
   - File system issues
   - Resource limitations

## Future Improvements

1. **Auto-Detection**
   - Tự động nhận diện question type
   - Suggest improvements cho format
   - Auto-correct common errors

2. **Batch Processing**
   - Import nhiều passages cùng lúc
   - Parallel processing
   - Progress tracking

3. **UI Integration**
   - Preview tool
   - Interactive editor
   - Real-time validation
