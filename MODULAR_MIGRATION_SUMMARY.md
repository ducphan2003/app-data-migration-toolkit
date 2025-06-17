# Modular Migration Logic Implementation

## Tổng quan

Đã thành công implement logic migrate dữ liệu IELTS theo từng question type riêng biệt, thay vì migrate toàn bộ cùng lúc. Điều này giúp:

1. **Modular và dễ maintain**: Mỗi question type có logic riêng biệt
2. **Scalable**: Dễ thêm question type mới  
3. **Debugging**: Dễ debug từng loại câu hỏi
4. **Performance**: Chỉ load rules cần thiết

## Cấu trúc Implementation

### 1. Methods mới được thêm vào `AIMigrationAgents`

#### A. Analysis Methods
- `analyze_question_types()`: Phân tích loại câu hỏi bằng AI hoặc fallback
- `_fallback_question_analysis()`: Fallback analysis khi AI không hoạt động
- `_simple_type_detection()`: Rule-based question type detection

#### B. Grouping & Migration Methods
- `_group_questions_by_type()`: Group questions theo question type
- `migrate_question_type()`: Migrate một nhóm questions cùng question_type
- `transform_to_question_sets_by_type()`: Orchestrate việc migration theo từng type

#### C. Type-specific Fallback Methods
- `_fallback_migrate_gap_filling()`: GAP_FILLING migration
- `_fallback_migrate_single_selection()`: SINGLE_SELECTION migration  
- `_fallback_migrate_matching()`: MATCHING migration
- `_fallback_migrate_multiple_choice_many()`: MULTIPLE_CHOICE_MANY migration
- `_fallback_migrate_note_completion()`: NOTE_COMPLETION migration
- `_fallback_migrate_single_choice()`: SINGLE_CHOICE migration
- `_fallback_migrate_generic()`: Generic fallback cho types khác

### 2. Question Types được hỗ trợ

1. **GAP_FILLING**: Câu hỏi điền từ vào chỗ trống
   - Detect: `gap_fill_in_blank` field + `type = "FILL-IN-THE-BLANK"`
   - Logic: Extract gaps, convert `{[answer][number]}` → `______`

2. **SINGLE_SELECTION**: True/False/Not Given questions
   - Detect: `type = "SINGLE-SELECTION"` + `selection_option` có TRUE/FALSE
   - Logic: Group consecutive questions với cùng options

3. **MATCHING**: Matching information questions  
   - Detect: `question_type = "MATCHING_INFO"`
   - Logic: Create options từ questions text → answer mapping

4. **MULTIPLE_CHOICE_MANY**: Multiple choice với nhiều đáp án đúng
   - Detect: `type = "MULTIPLE"` + `mutilple_choice` field
   - Logic: Extract correct answers, determine max_selections

5. **NOTE_COMPLETION**: Note completion với word list
   - Detect: `gap_fill_in_blank` có "List of words"
   - Logic: Extract vocabulary, separate từ main content

6. **SINGLE_CHOICE**: Single choice questions
   - Detect: `type = "SINGLE-RADIO"` + `single_choice_radio`
   - Logic: Each question có options riêng

### 3. Workflow

```
Input Data
    ↓
1. Analyze Question Types
    ↓
2. Group Questions by Type  
    ↓
3. Migrate Each Type Separately
    ↓
4. Combine Results
    ↓
Output: {quiz, parts, question_sets, questions}
```

## Test Results

### Test với GAP_FILLING data:
- ✅ Detected 1 GAP_FILLING question
- ✅ Successfully migrated to 1 question set và 7 questions
- ✅ Correct answers extracted: ["piston", "coal", "workshops", "labour", "quality", "railways", "sanitation"]
- ✅ Content converted từ `{[answer][number]}` → `______`
- ✅ Full database schema compliance

### Output Structure:
```json
{
  "quiz": { /* 30+ fields đầy đủ */ },
  "parts": [{ /* 18+ fields, content without gaps */ }],
  "question_sets": [{ 
    "question_type": "GAP_FILLING",
    "question_count": 7,
    "content": "content with ______ gaps"
  }],
  "questions": [{ 
    "question_type": "FILL_BLANK",
    "correct_answers": ["answer"],
    "quiz_id": 0,
    "part_id": null,
    "type": ""
  }]
}
```

## Rules Structure (Đề xuất tách file)

### Cấu trúc file rules mới:
```
import-data-tool/prompt/
├── base-migration-rules.md      # Migration rules by object  
├── gap_filling-rules.md         # GAP_FILLING specific rules
├── single_selection-rules.md    # SINGLE_SELECTION specific rules
├── matching-rules.md            # MATCHING specific rules
├── multiple_choice_many-rules.md
├── note_completion-rules.md
└── single_choice-rules.md
```

### Logic load rules:
```python
# Load base rules (common cho tất cả types)
base_rules = self._load_base_migration_rules()

# Load specific rules cho question type
type_rules = self._load_question_type_rules(question_type)

# Combine trong AI prompt
system_prompt = f"""
BASE MIGRATION RULES:
{base_rules}

SPECIFIC RULES FOR {question_type}:
{type_rules}
"""
```

## Benefits đạt được

1. **Maintainability**: Mỗi question type có logic riêng, dễ sửa đổi
2. **Extensibility**: Thêm question type mới chỉ cần implement fallback method
3. **Debugging**: Có thể test từng question type riêng biệt
4. **Performance**: AI agents chỉ cần xử lý một loại question tại một thời điểm
5. **Accuracy**: Rules specific cho từng type → kết quả chính xác hơn

## Next Steps

1. **Tách file rules** theo đề xuất cấu trúc trên
2. **Test với các question types khác** (SINGLE_SELECTION, MATCHING, etc.)
3. **Optimize AI prompts** cho từng question type
4. **Add validation** cho từng type migration result
5. **Performance monitoring** cho từng type migration

## Usage

```python
# Test modular migration
python test_modular_migration.py

# Results saved to:
import-data-tool/test-result/modular_migration_result_{timestamp}.json
``` 