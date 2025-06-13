# Quy tắc xác định cấu trúc và chuyển đổi dữ liệu IELTS

## 1. Quy tắc migrate theo đối tượng

### 1.1. Quiz
- **Giữ nguyên tất cả thông tin**
- **Các ngoại lệ**:
  - `vote_count`: Set = 0
  - `total_submitted`: Set = 0
  - `listening`: Bỏ qua, sẽ được chuyển vào `part.file_id`
  - `instruction_audio`: Bỏ qua, sẽ bổ sung sau

### 1.2. Parts
- **Các trường cần migrate**:
  - Giữ nguyên tất cả thông tin cơ bản
  - `file_id`: Lấy từ `quiz.listening`
- **Các trường bỏ qua**:
  - `questions`: Không cần vì sẽ sử dụng `question_sets`

### 1.3. Question Sets
- **Quy tắc gom nhóm**:
  - Gom các question lại thành các question_set
  - `part_id`: Lấy từ `part.id`
  - `question_type`: Xác định dựa trên loại câu hỏi
  - `question_count`: Số lượng question trong question_set
  - `title`: Format "Question " + question_from-question_to
    - Ví dụ: "Questions 1-7", "Questions 8-13"
  - `description`: Lấy từ đoạn hướng dẫn cách làm của loại câu hỏi đó

### 1.4. Questions
- **Giữ nguyên các thông tin cơ bản**
- **Các ngoại lệ**:
  - `quiz_id`: Set = 0
  - `part_id`: Set = null
  - `type`: Set = ""
  - `question_type`: Giữ nguyên như cũ
  - `gap_fill_in_blank`: Set = null
  - `correct_answer`: Sử dụng cho các loại:
    - SINGLE_SELECTION
    - MATCHING
    - NOTE_COMPLETION
    - SINGLE_CHOICE
  - `correct_answers`: Sử dụng cho các loại:
    - GAP_FILLING
    - MULTIPLE_CHOICE_MANY

## 2. Quy tắc migrate theo loại Question Set

### 2.1. GAP_FILLING
- **Xác định loại**:
  - Dựa vào `question_type` trong câu hỏi cũ
  - Nếu là "GAP_FILLING" thì tạo question_set mới với `question_type = "GAP_FILLING"`

- **Cấu trúc cũ**:
  ```json
  {
    "id": "question_id",
    "type": "FILL-IN-THE-BLANK",
    "question_type": "FILL_BLANK",
    "title": "Complete the notes below...",
    "gap_fill_in_blank": "<h3>Britain's Industrial Revolution</h3>...{[piston][1]}...{[coal][2]}...",
    "explain": "<div>Bước 1: Hiểu câu hỏi 1...</div><div>Bước 1: Hiểu câu hỏi 2...</div>"
  }
  ```

- **Cấu trúc mới**:
  ```json
  {
    "id": "auto_generate",
    "part_id": "part_id",
    "question_type": "GAP_FILLING",
    "question_count": "số lượng question trong set",
    "title": "Questions {from}-{to}",
    "description": "Lấy từ question.title cũ",
    "content": "<h3>Britain's Industrial Revolution</h3>...______...______...",
    "questions": [
      {
        "id": "auto_generate",
        "question_type": "GAP_FILLING",
        "correct_answers": ["piston"],
        "explanation": "<div>Bước 1: Hiểu câu hỏi 1...</div>"
      },
      {
        "id": "auto_generate",
        "question_type": "GAP_FILLING",
        "correct_answers": ["coal"],
        "explanation": "<div>Bước 1: Hiểu câu hỏi 2...</div>"
      }
    ]
  }
  ```

- **Quy tắc chuyển đổi**:
  1. **Question Set**:
     - `part_id`: Lấy từ part hiện tại
     - `question_type`: Set = "GAP_FILLING"
     - `question_count`: Đếm số lượng gap trong `gap_fill_in_blank` cũ
     - `title`: Format "Questions {from}-{to}" dựa trên số thứ tự câu hỏi
     - `description`: Lấy từ `title` của câu hỏi cũ
     - `content`: 
       - Lấy nội dung từ `gap_fill_in_blank` cũ
       - Thay thế các đáp án `{[answer][number]}` bằng `______`
       - Giữ nguyên cấu trúc HTML và định dạng

  2. **Questions**:
     - Tạo một question mới cho mỗi gap trong `gap_fill_in_blank` cũ
     - `question_type` là giá trị question_type của question cũ: question.question_type
     - `correct_answers`: 
       - Lấy đáp án từ `{[answer][number]}` trong `gap_fill_in_blank` cũ
       - Luôn ở dạng mảng
     - `explanation`: 
       - Phân tách `explain` cũ thành các phần riêng biệt cho từng câu hỏi
       - Mỗi phần giải thích tương ứng với một gap

- **Lưu ý**:
  - Cần đảm bảo thứ tự các câu hỏi trong set giống với thứ tự các gap trong `gap_fill_in_blank` cũ
  - Khi thay thế đáp án bằng `______`, cần giữ nguyên khoảng trắng và định dạng xung quanh
  - Cần xử lý các trường hợp đặc biệt như:
    - Nhiều đáp án đúng cho một gap (ví dụ: "labour | labor")
    - Đáp án có chứa ký tự đặc biệt hoặc định dạng HTML
    - Phần explanation có cấu trúc phức tạp cần được phân tách chính xác

### 2.2. SINGLE_SELECTION

- **Xác định loại**:
  - Dựa vào `type` trong câu hỏi cũ
  - Nếu là "SINGLE-SELECTION" thì tạo question_set mới với `question_type = "SINGLE_SELECTION"`

- **Cấu trúc cũ**:
  ```json
  {
    "id": "question_id",
    "type": "SINGLE-SELECTION",
    "question_type": "TRUE_FALSE",
    "title": "",
    "description": "<h2>Questions 8 - 13:</h2>\n<p>Do the following statements agree with the information given in Reading Passage 1?</p>\n<p>In boxes 8-13 on your answer sheet, write</p>\n<p><strong>TRUE</strong> if the statement agrees with the information</p>\n<p><strong>FALSE</strong> if the statement contradicts the information</p>\n<p><strong>NOT GIVEN</strong> if there is no information on this</p>",
    "selection": [
      {
        "text": "Britain's canal network grew rapidly so that more goods could be transported around the country.",
        "answer": "NOT GIVEN"
      }
    ],
    "selection_option": [
      {
        "option": "TRUE"
      },
      {
        "option": "FALSE"
      },
      {
        "option": "NOT GIVEN"
      }
    ],
    "explain": "<div>Bước 1: Hiểu câu hỏi...</div>"
  }
  ```

- **Cấu trúc mới**:
  ```json
  {
    "id": "auto_generate",
    "part_id": "part_id",
    "question_type": "SINGLE_SELECTION",
    "question_count": "số lượng question trong set",
    "title": "Questions {from}-{to}",
    "description": "Lấy từ question.description cũ của câu hỏi đầu tiên trong nhóm",
    "content": "",
    "option_title": "",
    "options": [
      {
        "text": "NO",
        "option": "FALSE"
      },
      {
        "text": "NOT GIVEN", 
        "option": "NOT GIVEN"
      },
      {
        "text": "YES",
        "option": "TRUE"
      }
    ],
    "allow_reuse": false,
    "max_selections": 0,
    "questions": [
      {
        "id": "auto_generate",
        "question_type": "TRUE_FALSE",
        "correct_answer": "NOT GIVEN",
        "text": "Britain's canal network grew rapidly so that more goods could be transported around the country.",
        "explanation": "<div>Bước 1: Hiểu câu hỏi...</div>"
      }
    ]
  }
  ```

- **Quy tắc chuyển đổi**:
  1. **Question Set**:
     - `part_id`: Lấy từ part hiện tại
     - `question_type`: Set = "SINGLE_SELECTION"
     - `question_count`: Đếm số lượng question cùng loại liên tiếp trong part
     - `title`: Format "Questions {from}-{to}" dựa trên số thứ tự câu hỏi
     - `description`: 
       - Lấy từ `description` của câu hỏi đầu tiên trong nhóm
       - Nếu không có thì lấy từ câu hỏi có `description` trong nhóm
       - Thay thế placeholder `{start_question}-{end_question}` bằng số thứ tự thực tế
     - `content`: Set = ""
     - `option_title`: Set = ""
     - `options`: 
       - Lấy từ `selection_option` của câu hỏi cũ
       - Chuyển đổi format từ `{"option": "value"}` thành `{"text": "display_text", "option": "value"}`
       - Đối với TRUE_FALSE: TRUE → "YES", FALSE → "NO", NOT GIVEN → "NOT GIVEN"
     - `allow_reuse`: Set = false
     - `max_selections`: Set = 0

  2. **Questions**:
     - Tạo một question mới cho mỗi câu hỏi cũ trong nhóm
     - `question_type`: Giữ nguyên từ câu hỏi cũ (ví dụ: "TRUE_FALSE")
     - `correct_answer`: 
       - Lấy từ `selection[0].answer` của câu hỏi cũ
       - Luôn ở dạng string đơn
     - `text`: Lấy từ `selection[0].text` của câu hỏi cũ
     - `explanation`: Lấy từ `explain` của câu hỏi cũ
     - Các trường khác:
       - `quiz_id`: Set = 0
       - `type`: Set = ""
       - `part_id`: Set = null
       - `correct_answers`: Set = null
       - `options`: Set = null

- **Quy tắc gom nhóm**:
  - Gom các question liên tiếp có cùng `type = "SINGLE-SELECTION"` và cùng `question_type`
  - Gom các question có cùng `selection_option` (cùng bộ lựa chọn)
  - Nếu có `description` ở câu hỏi đầu tiên thì sử dụng làm mốc để xác định nhóm
  - Ưu tiên gom theo thứ tự `sort` hoặc `order` liên tiếp

- **Lưu ý đặc biệt**:
  - Đối với TRUE_FALSE questions: 
    - Options luôn là ["YES", "NO", "NOT GIVEN"] với values tương ứng ["TRUE", "FALSE", "NOT GIVEN"]
  - Đối với các loại khác có thể có options khác nhau
  - Cần xử lý trường hợp `description` có placeholder `{start_question}-{end_question}` cần thay thế
  - Giữ nguyên HTML formatting trong `description` và `explanation`
  - Nếu một question không có `selection` hoặc `selection` rỗng thì bỏ qua question đó

### 2.3. MATCHING

- **Xác định loại**:
  - Dựa vào `question_type` trong câu hỏi cũ
  - Nếu là "MATCHING_INFO" thì tạo question_set mới với `question_type = "MATCHING"`

- **Cấu trúc cũ**:
  ```json
  {
    "id": "question_id",
    "type": "SINGLE-SELECTION",
    "question_type": "MATCHING_INFO",
    "title": "",
    "description": "<h2>Questions 14 - 18:</h2>\n<p>Reading Passage 2 has six paragraphs, A-F.</p>\n<p>Which paragraph contains the following information?</p>\n<p>Write the correct letter, A-F, in boxes 14-18 on your answer sheet.</p>\n<p><em><strong>NB</strong> You may use any letter more than once.</em></p>",
    "selection": [
      {
        "text": "reference to two chemical compounds which impact on performance",
        "answer": "D"
      }
    ],
    "selection_option": [
      {
        "option": "A"
      },
      {
        "option": "B"
      },
      {
        "option": "C"
      },
      {
        "option": "D"
      },
      {
        "option": "E"
      },
      {
        "option": "F"
      }
    ],
    "explain": "<div>Bước 1: Hiểu câu hỏi...</div>"
  }
  ```

- **Cấu trúc mới**:
  ```json
  {
    "id": "auto_generate",
    "part_id": "part_id",
    "question_type": "MATCHING",
    "question_count": "số lượng question trong set",
    "title": "Questions {from}-{to}",
    "description": "Lấy từ question.description cũ của câu hỏi đầu tiên trong nhóm",
    "content": "",
    "option_title": "",
    "options": [
      {
        "text": "reference to two chemical compounds which impact on performance",
        "option": "A"
      },
      {
        "text": "examples of strategies for minimising the effects of stress",
        "option": "B"
      }
    ],
    "allow_reuse": true,
    "max_selections": 0,
    "questions": [
      {
        "id": "auto_generate",
        "question_type": "MATCHING_INFO",
        "correct_answer": "D",
        "text": "",
        "explanation": "<div>Bước 1: Hiểu câu hỏi...</div>"
      }
    ]
  }
  ```

- **Quy tắc chuyển đổi**:
  1. **Question Set**:
     - `part_id`: Lấy từ part hiện tại
     - `question_type`: Set = "MATCHING"
     - `question_count`: Đếm số lượng question cùng loại liên tiếp trong part
     - `title`: Format "Questions {from}-{to}" dựa trên số thứ tự câu hỏi
     - `description`: 
       - Lấy từ `description` của câu hỏi đầu tiên trong nhóm
       - Thay thế placeholder `{start_question}-{end_question}` bằng số thứ tự thực tế
       - Giữ nguyên HTML formatting
     - `content`: Set = ""
     - `option_title`: Set = ""
     - `options`: 
       - Tạo từ tất cả `selection[0].text` của các câu hỏi trong nhóm
       - Format: `{"text": "question_text", "option": "answer_value"}`
       - `text`: Lấy từ `selection[0].text` của từng câu hỏi
       - `option`: Lấy từ `selection[0].answer` của từng câu hỏi tương ứng
     - `allow_reuse`: Set = true (vì thường có thể dùng lại đáp án)
     - `max_selections`: Set = 0

  2. **Questions**:
     - Tạo một question mới cho mỗi câu hỏi cũ trong nhóm
     - `question_type`: Giữ nguyên từ câu hỏi cũ (ví dụ: "MATCHING_INFO")
     - `correct_answer`: 
       - Lấy từ `selection[0].answer` của câu hỏi cũ
       - Luôn ở dạng string đơn
     - `text`: Set = "" (vì text đã được chuyển vào options của question_set)
     - `explanation`: Lấy từ `explain` của câu hỏi cũ
     - Các trường khác:
       - `quiz_id`: Set = 0
       - `type`: Set = ""
       - `part_id`: Set = null
       - `correct_answers`: Set = null
       - `options`: Set = null

- **Quy tắc gom nhóm**:
  - Gom các question liên tiếp có cùng `question_type = "MATCHING_INFO"`
  - Gom các question có cùng `selection_option` (cùng bộ lựa chọn A, B, C, D, E, F...)
  - Nếu có `description` ở câu hỏi đầu tiên thì sử dụng làm mốc để xác định nhóm
  - Ưu tiên gom theo thứ tự `sort` hoặc `order` liên tiếp

- **Lưu ý đặc biệt**:
  - Đối với MATCHING_INFO: 
    - Options được tạo từ các câu hỏi (text) và đáp án tương ứng
    - Thường có `allow_reuse = true` vì có thể dùng lại đáp án
  - Cần xử lý trường hợp `description` có placeholder `{start_question}-{end_question}` cần thay thế
  - Giữ nguyên HTML formatting trong `description` và `explanation`
  - Nếu một question không có `selection` hoặc `selection` rỗng thì bỏ qua question đó
  - Thứ tự trong `options` phải tương ứng với thứ tự các question trong `questions`

### 2.4. MULTIPLE_CHOICE_MANY

- **Xác định loại**:
  - Dựa vào `type` và `question_type` trong câu hỏi cũ
  - Nếu là `type = "MULTIPLE"` và `question_type = "MULTIPLE_CHOICE_MANY"` thì tạo question_set mới với `question_type = "MULTIPLE_CHOICE_MANY"`

- **Cấu trúc cũ**:
  ```json
  {
    "id": "question_id",
    "type": "MULTIPLE",
    "question_type": "MULTIPLE_CHOICE_MANY",
    "title": "Which TWO facts about Emma Raducanu's withdrawal from the Wimbledon tournament are mentioned in the text?",
    "description": "<h2>Questions 23 - 24:</h2>\n<p>Choose TWO letters, A-E.</p>\n<p>Write the correct letters in boxes 23 - 24 on your answer sheet.</p>",
    "mutilple_choice": [
      {
        "text": "the stage at which she dropped out of the tournament",
        "correct": false,
        "order": 1
      },
      {
        "text": "symptoms of her performance stress at the tournament",
        "correct": true,
        "order": 2,
        "explain": "<div>Bước 1: Hiểu yêu cầu câu hỏi...</div>"
      },
      {
        "text": "aspects of the Wimbledon tournament which increased her stress levels",
        "correct": true,
        "order": 4,
        "explain": "<div>Bước 1: Hiểu yêu cầu câu hỏi...</div>"
      }
    ],
    "explain": null
  }
  ```

- **Cấu trúc mới**:
  ```json
  {
    "id": "auto_generate",
    "part_id": "part_id",
    "question_type": "MULTIPLE_CHOICE_MANY",
    "question_count": "số lượng question trong set",
    "title": "Questions {from}-{to}",
    "description": "Lấy từ question.description cũ",
    "content": "",
    "option_title": "",
    "options": [
      {
        "text": "the stage at which she dropped out of the tournament",
        "option": "A"
      },
      {
        "text": "symptoms of her performance stress at the tournament",
        "option": "B"
      }
    ],
    "allow_reuse": false,
    "max_selections": 2,
    "questions": [
      {
        "id": "auto_generate",
        "question_type": "MULTIPLE",
        "correct_answers": ["B", "D"],
        "text": "",
        "explanation": "Tổng hợp từ explain của các options đúng"
      }
    ]
  }
  ```

- **Quy tắc chuyển đổi**:
  1. **Question Set**:
     - `part_id`: Lấy từ part hiện tại
     - `question_type`: Set = "MULTIPLE_CHOICE_MANY"
     - `question_count`: Đếm số lượng question cùng loại liên tiếp trong part
     - `title`: Format "Questions {from}-{to}" dựa trên số thứ tự câu hỏi
     - `description`: 
       - Lấy từ `description` của câu hỏi cũ
       - Thay thế placeholder `{start_question}-{end_question}` bằng số thứ tự thực tế
       - Giữ nguyên HTML formatting
     - `content`: Set = ""
     - `option_title`: Set = ""
     - `options`: 
       - Tạo từ tất cả items trong `mutilple_choice` của câu hỏi cũ
       - Format: `{"text": "option_text", "option": "letter"}`
       - `text`: Lấy từ `mutilple_choice[i].text`
       - `option`: Tạo letter tự động theo thứ tự A, B, C, D, E...
       - Sắp xếp theo `mutilple_choice[i].order`
     - `allow_reuse`: Set = false (không thể chọn lại cùng đáp án)
     - `max_selections`: Lấy từ số lượng đáp án đúng hoặc từ description (ví dụ: "Choose TWO" → 2)

  2. **Questions**:
     - Tạo một question duy nhất cho toàn bộ question set
     - `question_type`: Set = "MULTIPLE"
     - `correct_answers`: 
       - Lấy tất cả options có `correct = true` từ `mutilple_choice`
       - Chuyển thành array các letters tương ứng (A, B, C...)
       - Ví dụ: nếu option thứ 2 và 4 đúng → ["B", "D"]
     - `text`: Set = "" (vì text đã có trong title của question_set)
     - `explanation`: 
       - Tổng hợp từ `explain` của các options có `correct = true`
       - Nếu không có explain riêng cho options, lấy từ `explain` chung của question
       - Format: kết hợp các explanation thành một đoạn dài
     - Các trường khác:
       - `quiz_id`: Set = 0
       - `type`: Set = ""
       - `part_id`: Set = null
       - `correct_answer`: Set = ""
       - `options`: Set = null

- **Quy tắc gom nhóm**:
  - Thường mỗi MULTIPLE_CHOICE_MANY là một question set riêng biệt
  - Chỉ gom nhóm nếu có nhiều questions liên tiếp cùng loại và cùng chủ đề
  - Ưu tiên gom theo thứ tự `sort` hoặc `order` liên tiếp

- **Lưu ý đặc biệt**:
  - Đối với MULTIPLE_CHOICE_MANY:
    - `max_selections` phải được xác định chính xác từ description hoặc đếm số đáp án đúng
    - Options được sắp xếp theo `order` trong `mutilple_choice`
    - Chỉ có một question trong question_set nhưng có nhiều đáp án đúng
  - Cần xử lý trường hợp `description` có placeholder cần thay thế
  - Giữ nguyên HTML formatting trong `description` và `explanation`
  - Nếu một option không có `text` thì bỏ qua option đó
  - Explanation có thể được tổng hợp từ nhiều options hoặc lấy từ explain chung

### 2.5. NOTE_COMPLETION

- **Xác định loại**:
  - Dựa vào `type` và `question_type` trong câu hỏi cũ
  - Nếu là `type = "FILL-IN-THE-BLANK"` và `question_type = "FILL_BLANK"` với có `gap_fill_in_blank` chứa danh sách từ vựng thì tạo question_set mới với `question_type = "NOTE_COMPLETION"`

- **Cấu trúc cũ**:
  ```json
  {
    "id": "question_id",
    "type": "FILL-IN-THE-BLANK",
    "question_type": "FILL_BLANK",
    "title": "Complete the summary using the list of phrases, A- K, below. Write the correct letter, A- K, in boxes 27 - 32 on your answer sheet.",
    "description": "<h2>Questions 27 - 32:</h2>",
    "gap_fill_in_blank": "<h3>List of words</h3>\n<table>\n<tr><td><strong>A</strong> appeal</td><td><strong>B</strong> determined</td></tr>\n<tr><td><strong>C</strong> intrigued</td><td><strong>D</strong> single</td></tr>\n</table>\n<h3>Maryam Mirzakhani</h3>\n<p>Maryam Mirzakhani is regarded as {[H][27]} in the field of mathematics...</p>",
    "explain": "<div>Câu 27: Bước 1: Hiểu câu hỏi...</div>"
  }
  ```

- **Cấu trúc mới**:
  ```json
  {
    "id": "auto_generate",
    "part_id": "part_id",
    "question_type": "NOTE_COMPLETION",
    "question_count": "số lượng gaps trong content",
    "title": "Questions {from}-{to}",
    "description": "Lấy từ title cũ hoặc tạo mới",
    "content": "<h3><strong>Notes on Maryam Mirzakhani</strong></h3>\n<div class=\"note-completion-content\">\n<p>Maryam Mirzakhani is regarded as <span class=\"gap-placeholder\" data-question-id=\"note_comp_27\">______</span> in the field of mathematics...</p>\n</div>",
    "option_title": "",
    "options": [
      {
        "text": "appeal",
        "option": "A"
      },
      {
        "text": "determined",
        "option": "B"
      }
    ],
    "allow_reuse": true,
    "max_selections": 0,
    "questions": [
      {
        "id": "auto_generate",
        "question_type": "NOTE_COMPLETION",
        "correct_answer": "H",
        "text": "",
        "explanation": "Bước 1: Hiểu câu hỏi..."
      }
    ]
  }
  ```

- **Quy tắc chuyển đổi**:
  1. **Question Set**:
     - `part_id`: Lấy từ part hiện tại
     - `question_type`: Set = "NOTE_COMPLETION"
     - `question_count`: Đếm số lượng gaps trong `gap_fill_in_blank` (đếm {[letter][number]})
     - `title`: Format "Questions {from}-{to}" dựa trên số thứ tự câu hỏi
     - `description`: 
       - Lấy từ `title` của câu hỏi cũ hoặc tạo mới
       - Thay thế placeholder `{start_question}-{end_question}` bằng số thứ tự thực tế
       - Format: "Complete the notes below. Choose NO MORE THAN ONE WORD from the passage for each answer."
     - `content`: 
       - Lấy nội dung từ `gap_fill_in_blank` cũ
       - Loại bỏ phần "List of words" (bảng từ vựng)
       - Chuyển đổi `{[letter][number]}` thành `<span class="gap-placeholder" data-question-id="note_comp_{number}">______</span>`
       - Thêm wrapper `<div class="note-completion-content">` và cấu trúc notes
     - `option_title`: Set = ""
     - `options`: 
       - Trích xuất từ bảng "List of words" trong `gap_fill_in_blank`
       - Format: `{"text": "word", "option": "letter"}`
       - Sắp xếp theo thứ tự A, B, C, D...
     - `allow_reuse`: Set = true (có thể dùng lại từ vựng)
     - `max_selections`: Set = 0

  2. **Questions**:
     - Tạo một question cho mỗi gap trong `gap_fill_in_blank`
     - `question_type`: Set = "NOTE_COMPLETION"
     - `correct_answer`: 
       - Lấy từ `{[letter][number]}` trong `gap_fill_in_blank` cũ
       - Chỉ lấy letter (A, B, C...) hoặc từ tương ứng
     - `text`: Set = "" (vì text đã có trong content của question_set)
     - `explanation`: 
       - Trích xuất từ `explain` của câu hỏi cũ
       - Phân tách theo từng câu (Câu 27, Câu 28...)
       - Mỗi question có explanation riêng
     - Các trường khác:
       - `quiz_id`: Set = 0
       - `type`: Set = ""
       - `part_id`: Set = null
       - `correct_answers`: Set = null
       - `options`: Set = null

- **Quy tắc gom nhóm**:
  - Thường mỗi NOTE_COMPLETION là một question set riêng biệt
  - Chỉ gom nhóm nếu có nhiều questions liên tiếp cùng loại và cùng bảng từ vựng
  - Ưu tiên gom theo thứ tự `sort` hoặc `order` liên tiếp

- **Lưu ý đặc biệt**:
  - Đối với NOTE_COMPLETION:
    - Cần tách riêng "List of words" và nội dung chính từ `gap_fill_in_blank`
    - Chuyển đổi format gap từ `{[letter][number]}` sang `<span class="gap-placeholder">`
    - Options được trích xuất từ bảng từ vựng, không phải từ nội dung
    - Explanation cần được phân tách theo từng câu hỏi
  - Cần xử lý trường hợp `description` có placeholder cần thay thế
  - Giữ nguyên HTML formatting trong `content` và `explanation`
  - Nếu không có bảng từ vựng thì có thể là dạng GAP_FILLING thay vì NOTE_COMPLETION
  - Thứ tự questions phải tương ứng với thứ tự gaps trong content

### 2.6. SINGLE_CHOICE

- **Xác định loại**:
  - Dựa vào `type` và `question_type` trong câu hỏi cũ
  - Nếu là `type = "SINGLE-RADIO"` và `question_type = "MULTIPLE_CHOICE_ONE"` thì tạo question_set mới với `question_type = "SINGLE_CHOICE"`

- **Cấu trúc cũ**:
  ```json
  {
    "id": "question_id",
    "type": "SINGLE-RADIO",
    "question_type": "MULTIPLE_CHOICE_ONE",
    "title": "What does Eyre believe is needed for children to equal 'gifted' standards?",
    "description": "<h2>Questions 38 - 40:</h2>\n<p>Choose the correct letter, A, B, C or D.</p>\n<p>Write the correct letter in boxes 38 - 40 on your answer sheet.</p>",
    "single_choice_radio": [
      {
        "text": "strict discipline from the teaching staff",
        "correct": false
      },
      {
        "text": "the development of a spirit of inquiry towards their studies",
        "correct": true
      }
    ],
    "explain": "<div>Bước 1: Hiểu và tìm keywords trong câu hỏi...</div>"
  }
  ```

- **Cấu trúc mới**:
  ```json
  {
    "id": "auto_generate",
    "part_id": "part_id",
    "question_type": "SINGLE_CHOICE",
    "question_count": "số lượng question trong set",
    "title": "Questions {from}-{to}",
    "description": "Lấy từ question.description cũ của câu hỏi đầu tiên trong nhóm",
    "content": "",
    "option_title": "",
    "options": null,
    "allow_reuse": false,
    "max_selections": 0,
    "questions": [
      {
        "id": "auto_generate",
        "question_type": "SINGLE-CHOICE",
        "correct_answer": "C",
        "text": "What does Eyre believe is needed for children to equal 'gifted' standards?",
        "options": [
          {
            "text": "strict discipline from the teaching staff",
            "option": "A",
            "is_correct": false
          },
          {
            "text": "the development of a spirit of inquiry towards their studies",
            "option": "C",
            "is_correct": true
          }
        ],
        "explanation": "<div>Bước 1: Hiểu và tìm keywords trong câu hỏi...</div>"
      }
    ]
  }
  ```

- **Quy tắc chuyển đổi**:
  1. **Question Set**:
     - `part_id`: Lấy từ part hiện tại
     - `question_type`: Set = "SINGLE_CHOICE"
     - `question_count`: Đếm số lượng question cùng loại liên tiếp trong part
     - `title`: Format "Questions {from}-{to}" dựa trên số thứ tự câu hỏi
     - `description`: 
       - Lấy từ `description` của câu hỏi đầu tiên trong nhóm
       - Thay thế placeholder `{start_question}-{end_question}` bằng số thứ tự thực tế
       - Giữ nguyên HTML formatting
     - `content`: Set = ""
     - `option_title`: Set = ""
     - `options`: Set = null (vì mỗi question có options riêng)
     - `allow_reuse`: Set = false
     - `max_selections`: Set = 0

  2. **Questions**:
     - Tạo một question cho mỗi câu hỏi cũ trong nhóm
     - `question_type`: Set = "SINGLE-CHOICE"
     - `correct_answer`: 
       - Tìm option có `correct = true` trong `single_choice_radio`
       - Chuyển thành letter tương ứng (A, B, C, D...)
     - `text`: Lấy từ `title` của câu hỏi cũ
     - `options`: 
       - Chuyển đổi từ `single_choice_radio` của câu hỏi cũ
       - Format: `{"text": "option_text", "option": "letter", "is_correct": boolean}`
       - Sắp xếp theo thứ tự A, B, C, D...
     - `explanation`: Lấy từ `explain` của câu hỏi cũ
     - Các trường khác:
       - `quiz_id`: Set = 0
       - `type`: Set = ""
       - `part_id`: Set = null
       - `correct_answers`: Set = null

- **Quy tắc gom nhóm**:
  - Gom các question liên tiếp có cùng `type = "SINGLE-RADIO"` và `question_type = "MULTIPLE_CHOICE_ONE"`
  - Gom các question có cùng `description` (cùng nhóm câu hỏi)
  - Nếu có `description` ở câu hỏi đầu tiên thì sử dụng làm mốc để xác định nhóm
  - Ưu tiên gom theo thứ tự `sort` hoặc `order` liên tiếp

- **Lưu ý đặc biệt**:
  - Đối với SINGLE_CHOICE:
    - Mỗi question có options riêng biệt (khác với SINGLE_SELECTION có options chung)
    - Options được sắp xếp theo thứ tự A, B, C, D...
    - Chỉ có một đáp án đúng cho mỗi question
    - `text` của question lấy từ `title` của câu hỏi cũ
  - Cần xử lý trường hợp `description` có placeholder cần thay thế
  - Giữ nguyên HTML formatting trong `description` và `explanation`
  - Nếu một question không có `single_choice_radio` hoặc rỗng thì bỏ qua question đó
  - Thứ tự options phải được sắp xếp theo alphabet (A, B, C, D...)

