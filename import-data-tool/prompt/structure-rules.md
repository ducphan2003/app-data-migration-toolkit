# Rules for defining IELTS data structure and transformation

## 1. Migration rules by object

### 1.1. Quiz
- **Keep all information**
- **Exceptions**:
  - `vote_count`: Set = 0
  - `total_submitted`: Set = 0
  - `listening`: Skip, will be transferred to `part.file_id`
  - `instruction_audio`: Skip, will be added later

### 1.2. Parts
- **Fields to migrate**:
  - Keep all basic information
  - `file_id`: Take from `quiz.listening`
- **Fields to skip**:
  - `questions`: Not needed because `question_sets` will be used

### 1.3. Question Sets
- **Grouping rules**:
  - Group questions into question_sets
  - `part_id`: Take from `part.id`
  - `question_type`: Determine based on question type
  - `question_count`: Number of questions in question_set
  - `title`: Format "Question " + question_from-question_to
    - Example: "Questions 1-7", "Questions 8-13"
  - `description`: Take from the instruction of the question type

### 1.4. Questions
- **Keep all basic information**
- **Exceptions**:
  - `quiz_id`: Set = 0
  - `part_id`: Set = null
  - `type`: Set = ""
  - `question_type`: Keep as is
  - `gap_fill_in_blank`: Set = null
  - `correct_answer`: Used for the following types:
    - SINGLE_SELECTION
    - MATCHING
    - NOTE_COMPLETION
    - SINGLE_CHOICE
  - `correct_answers`: Used for the following types:
    - GAP_FILLING
    - MULTIPLE_CHOICE_MANY

## 2. Migration rules by question set type

### 2.1. GAP_FILLING
- **Determine type**:
  - Based on `question_type` in the old question
  - If it is "GAP_FILLING" then create a new question_set with `question_type = "GAP_FILLING"`

- **Old structure**:
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
    "question_count": "number of questions in the set",
    "title": "Questions {from}-{to}",
    "description": "Take from question.title of the old question",
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

- **Migration rules**:
  1. **Question Set**:
     - `part_id`: Take from the current part
     - `question_type`: Set = "GAP_FILLING"
     - `question_count`: Count the number of gaps in the old `gap_fill_in_blank`
     - `title`: Format "Questions {from}-{to}" based on the question order
     - `description`: Take from the old question.title
     - `content`: 
       - Take the content from the old `gap_fill_in_blank`
       - Replace the answers `{[answer][number]}` with `______`
       - Keep the HTML structure and formatting

  2. **Questions**:
     - Create a new question for each gap in the old `gap_fill_in_blank`
     - `question_type` is the value of question_type of the old question: question.question_type
     - `correct_answers`: 
       - Take the answer from the old `{[answer][number]}` in the `gap_fill_in_blank`
       - Always in array format
     - `explanation`: 
       - Split the old `explain` into separate parts for each question
       - Each explanation corresponds to one gap

- **Notes**:
  - Ensure the order of questions in the set is the same as the order of gaps in the old `gap_fill_in_blank`
  - When replacing the answer with `______`, keep the spaces and formatting around
  - Handle special cases such as:
    - Multiple correct answers for one gap (e.g. "labour | labor")
    - Answer contains special characters or HTML formatting
    - The explanation has a complex structure and needs to be accurately split

### 2.2. SINGLE_SELECTION

- **Determine type**:
  - Based on `type` in the old question
  - If it is "SINGLE-SELECTION" then create a new question_set with `question_type = "SINGLE_SELECTION"`

- **Old structure**:
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

- **New structure**:
  ```json
  {
    "id": "auto_generate",
    "part_id": "part_id",
    "question_type": "SINGLE_SELECTION",
    "question_count": "number of questions in the set",
    "title": "Questions {from}-{to}",
    "description": "Take from the old question.description of the first question in the group",
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

- **Migration rules**:
  1. **Question Set**:
     - `part_id`: Take from the current part
     - `question_type`: Set = "SINGLE_SELECTION"
     - `question_count`: Count the number of questions of the same type consecutively in the part
     - `title`: Format "Questions {from}-{to}" based on the question order
     - `description`: 
       - Take from the old question.description of the first question in the group
       - If there is no description, take from the question with `description` in the group
       - Replace the placeholder `{start_question}-{end_question}` with the actual order
     - `content`: Set = ""
     - `option_title`: Set = ""
     - `options`: 
       - Take from the old question.selection_option
       - Convert the format from `{"option": "value"}` to `{"text": "display_text", "option": "value"}`
       - For TRUE_FALSE: TRUE → "YES", FALSE → "NO", NOT GIVEN → "NOT GIVEN"
     - `allow_reuse`: Set = false
     - `max_selections`: Set = 0

  2. **Questions**:
     - Create a new question for each old question in the group
     - `question_type`: Keep the old question.question_type (e.g. "TRUE_FALSE")
     - `correct_answer`: 
       - Take from the old question.selection[0].answer
       - Always in string format
     - `text`: Take from the old question.selection[0].text
     - `explanation`: Take from the old question.explain
     - Other fields:
       - `quiz_id`: Set = 0
       - `type`: Set = ""
       - `part_id`: Set = null
       - `correct_answers`: Set = null
       - `options`: Set = null

- **Grouping rules**:
  - Group questions consecutively with the same `type = "SINGLE-SELECTION"` and the same `question_type`
  - Group questions with the same `selection_option` (same options)
  - If there is a `description` in the first question, use it as the basis for determining the group
  - Prefer to group by `sort` or `order` consecutively

- **Notes**:
  - For TRUE_FALSE questions: 
    - Options are always ["YES", "NO", "NOT GIVEN"] with corresponding values ["TRUE", "FALSE", "NOT GIVEN"]
  - For other types, there may be different options
  - Handle the case where `description` has a placeholder `{start_question}-{end_question}` and need to replace
  - Keep HTML formatting in `description` and `explanation`
  - If a question has no `selection` or `selection` is empty, skip the question

### 2.3. MATCHING

- **Determine type**:
  - Based on `question_type` in the old question
  - If it is "MATCHING_INFO" then create a new question_set with `question_type = "MATCHING"`

- **Old structure**:
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

- **New structure**:
  ```json
  {
    "id": "auto_generate",
    "part_id": "part_id",
    "question_type": "MATCHING",
    "question_count": "number of questions in the set",
    "title": "Questions {from}-{to}",
    "description": "Take from the old question.description of the first question in the group",
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

- **Migration rules**:
  1. **Question Set**:
     - `part_id`: Take from the current part
     - `question_type`: Set = "MATCHING"
     - `question_count`: Count the number of questions of the same type consecutively in the part
     - `title`: Format "Questions {from}-{to}" based on the question order
     - `description`: 
       - Take from the old question.description of the first question in the group
       - Replace the placeholder `{start_question}-{end_question}` with the actual order
       - Keep HTML formatting
     - `content`: Set = ""
     - `option_title`: Set = ""
     - `options`: 
       - Create from all `selection[0].text` of the questions in the group
       - Format: `{"text": "question_text", "option": "answer_value"}`
       - `text`: Take from the old question.selection[0].text of each question
       - `option`: Take from the old question.selection[0].answer of each question
     - `allow_reuse`: Set = true (because it can reuse the answer)
     - `max_selections`: Set = 0

  2. **Questions**:
     - Create a new question for each old question in the group
     - `question_type`: Keep the old question.question_type (e.g. "MATCHING_INFO")
     - `correct_answer`: 
       - Take from the old question.selection[0].answer
       - Always in string format
     - `text`: Set = "" (because the text has been transferred to the options of the question_set)
     - `explanation`: Take from the old question.explain
     - Other fields:
       - `quiz_id`: Set = 0
       - `type`: Set = ""
       - `part_id`: Set = null
       - `correct_answers`: Set = null
       - `options`: Set = null

- **Grouping rules**:
  - Group questions consecutively with the same `question_type = "MATCHING_INFO"`
  - Group questions with the same `selection_option` (same options A, B, C, D, E, F...)
  - If there is a `description` in the first question, use it as the basis for determining the group
  - Prefer to group by `sort` or `order` consecutively

- **Notes**:
  - For MATCHING_INFO: 
    - Options are created from the questions (text) and corresponding answers
    - Usually has `allow_reuse = true` because it can reuse the answer
  - Handle the case where `description` has a placeholder `{start_question}-{end_question}` and need to replace
  - Keep HTML formatting in `description` and `explanation`
  - If a question has no `selection` or `selection` is empty, skip the question
  - The order in `options` must correspond to the order of questions in `questions`

### 2.4. MULTIPLE_CHOICE_MANY

- **Determine type**:
  - Based on `type` and `question_type` in the old question
  - If it is `type = "MULTIPLE"` and `question_type = "MULTIPLE_CHOICE_MANY"` then create a new question_set with `question_type = "MULTIPLE_CHOICE_MANY"`

- **Old structure**:
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

- **New structure**:
  ```json
  {
    "id": "auto_generate",
    "part_id": "part_id",
    "question_type": "MULTIPLE_CHOICE_MANY",
    "question_count": "number of questions in the set",
    "title": "Questions {from}-{to}",
    "description": "Take from the old question.description",
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

- **Migration rules**:
  1. **Question Set**:
     - `part_id`: Take from the current part
     - `question_type`: Set = "MULTIPLE_CHOICE_MANY"
     - `question_count`: Count the number of questions of the same type consecutively in the part
     - `title`: Format "Questions {from}-{to}" based on the question order
     - `description`: 
       - Take from the old question.description
       - Replace the placeholder `{start_question}-{end_question}` with the actual order
       - Keep HTML formatting
     - `content`: Set = ""
     - `option_title`: Set = ""
     - `options`: 
       - Create from all items in the old question.mutilple_choice
       - Format: `{"text": "option_text", "option": "letter"}`
       - `text`: Take from the old question.mutilple_choice[i].text
       - `option`: Create letter automatically in the order A, B, C, D, E...
       - Sort by the old question.mutilple_choice[i].order
     - `allow_reuse`: Set = false (cannot reuse the same answer)
     - `max_selections`: Take from the number of correct answers or from the description (e.g. "Choose TWO" → 2)

  2. **Questions**:
     - Create a single question for the entire question set
     - `question_type`: Set = "MULTIPLE"
     - `correct_answers`: 
       - Take all options with `correct = true` from the old question.mutilple_choice
       - Convert to an array of letters corresponding to (A, B, C...)
       - Example: if option 2 and 4 are correct → ["B", "D"]
     - `text`: Set = "" (because the text is in the title of the question_set)
     - `explanation`: 
       - Combine the explanations of the options with `correct = true`
       - If there is no explanation for the options, take from the old question.explain
       - Format: combine the explanations into a long paragraph
     - Other fields:
       - `quiz_id`: Set = 0
       - `type`: Set = ""
       - `part_id`: Set = null
       - `correct_answer`: Set = ""
       - `options`: Set = null

- **Grouping rules**:
  - Usually each MULTIPLE_CHOICE_MANY is a separate question set
  - Only group if there are many questions consecutively of the same type and same topic
  - Prefer to group consecutively by `sort` or `order`

- **Notes**:
  - For MULTIPLE_CHOICE_MANY:
    - `max_selections` must be determined accurately from the description or count the number of correct answers
    - Options are sorted by the `order` in the old question.mutilple_choice
    - There is only one question in the question_set but there are many correct answers
  - Need to handle the case where `description` has a placeholder that needs to be replaced
  - Keep HTML formatting in `description` and `explanation`
  - If an option has no `text`, skip the option
  - Explanation can be combined from many options or taken from the old question.explain

### 2.5. NOTE_COMPLETION

- **Determine type**:
  - Based on `type` and `question_type` in the old question
  - If it is `type = "FILL-IN-THE-BLANK"` and `question_type = "FILL_BLANK"` and has `gap_fill_in_blank` containing the vocabulary list then create a new question_set with `question_type = "NOTE_COMPLETION"`

- **Old structure**:
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

- **New structure**:
  ```json
  {
    "id": "auto_generate",
    "part_id": "part_id",
    "question_type": "NOTE_COMPLETION",
    "question_count": "number of gaps in the content",
    "title": "Questions {from}-{to}",
    "description": "Take from the old question.title or create new",
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

- **Migration rules**:
  1. **Question Set**:
     - `part_id`: Take from the current part
     - `question_type`: Set = "NOTE_COMPLETION"
     - `question_count`: Count the number of gaps in the `gap_fill_in_blank` (count {[letter][number]})
     - `title`: Format "Questions {from}-{to}" based on the question order
     - `description`: 
       - Take from the old question.title or create new
       - Replace the placeholder `{start_question}-{end_question}` with the actual order
       - Format: "Complete the notes below. Choose NO MORE THAN ONE WORD from the passage for each answer."
     - `content`: 
       - Take from the old question.gap_fill_in_blank
       - Remove the "List of words" (vocabulary table)
       - Convert `{[letter][number]}` to `<span class="gap-placeholder" data-question-id="note_comp_{number}">______</span>`
       - Add wrapper `<div class="note-completion-content">` and structure notes
     - `option_title`: Set = ""
     - `options`: 
       - Extract from the "List of words" in the `gap_fill_in_blank`
       - Format: `{"text": "word", "option": "letter"}`
       - Sort by the order A, B, C, D...
     - `allow_reuse`: Set = true (can reuse the vocabulary)
     - `max_selections`: Set = 0

  2. **Questions**:
     - Create a question for each gap in the `gap_fill_in_blank`
     - `question_type`: Set = "NOTE_COMPLETION"
     - `correct_answer`: 
       - Take from the `{[letter][number]}` in the old question.gap_fill_in_blank
       - Only take letter (A, B, C...) or corresponding word
     - `text`: Set = "" (because the text is in the content of the question_set)
     - `explanation`: 
       - Extract from the old question.explain
       - Split by question (Question 27, Question 28...)
       - Each question has a separate explanation
     - Các trường khác:
       - `quiz_id`: Set = 0
       - `type`: Set = ""
       - `part_id`: Set = null
       - `correct_answers`: Set = null
       - `options`: Set = null

- **Grouping rules**:
  - Usually each NOTE_COMPLETION is a separate question set
  - Only group if there are many questions consecutively of the same type and same vocabulary
  - Prefer to group consecutively by `sort` or `order`

- **Notes**:
  - For NOTE_COMPLETION:
    - Need to separate the "List of words" and main content from the `gap_fill_in_blank`
    - Convert gap format from `{[letter][number]}` to `<span class="gap-placeholder">`
    - Options are extracted from the vocabulary table, not from the content
    - Explanation needs to be split by question
  - Need to handle the case where `description` has a placeholder that needs to be replaced
  - Keep HTML formatting in `content` and `explanation`
  - If there is no vocabulary table, it may be a GAP_FILLING instead of NOTE_COMPLETION
  - The order of questions must correspond to the order of gaps in the content

### 2.6. SINGLE_CHOICE

- **Determine type**:
  - Based on `type` and `question_type` in the old question
  - If it is `type = "SINGLE-RADIO"` and `question_type = "MULTIPLE_CHOICE_ONE"` then create a new question_set with `question_type = "SINGLE_CHOICE"`

- **Old structure**:
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

- **New structure**:
  ```json
  {
    "id": "auto_generate",
    "part_id": "part_id",
    "question_type": "SINGLE_CHOICE",
    "question_count": "number of questions in the set",
    "title": "Questions {from}-{to}",
    "description": "Take from the old question.description of the first question in the group",
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

- **Migration rules**:
  1. **Question Set**:
     - `part_id`: Take from the current part
     - `question_type`: Set = "SINGLE_CHOICE"
     - `question_count`: Count the number of questions consecutively of the same type in the part
     - `title`: Format "Questions {from}-{to}" based on the question order
     - `description`: 
       - Take from the old question.description of the first question in the group
       - Replace the placeholder `{start_question}-{end_question}` with the actual order
       - Keep HTML formatting
     - `content`: Set = ""
     - `option_title`: Set = ""
     - `options`: Set = null (because each question has separate options)
     - `allow_reuse`: Set = false
     - `max_selections`: Set = 0

  2. **Questions**:
     - Create a question for each old question in the group
     - `question_type`: Set = "SINGLE-CHOICE"
     - `correct_answer`: 
       - Find the option with `correct = true` in the old question.single_choice_radio
       - Convert to the corresponding letter (A, B, C, D...)
     - `text`: Take from the old question.title
     - `options`: 
       - Convert from the old question.single_choice_radio
       - Format: `{"text": "option_text", "option": "letter", "is_correct": boolean}`
       - Sort by the order A, B, C, D...
     - `explanation`: Take from the old question.explain
     - Other fields:
       - `quiz_id`: Set = 0
       - `type`: Set = ""
       - `part_id`: Set = null
       - `correct_answers`: Set = null

- **Grouping rules**:
  - Group consecutive questions with `type = "SINGLE-RADIO"` and `question_type = "MULTIPLE_CHOICE_ONE"`
  - Group questions with the same `description` (same question group)
  - If there is a `description` in the first question, use it as the basis for determining the group
  - Prefer to group consecutively by `sort` or `order`

- **Notes**:
  - For SINGLE_CHOICE:
    - Each question has separate options (different from SINGLE_SELECTION which has common options)
    - Options are sorted by the order A, B, C, D...
    - There is only one correct answer for each question
    - `text` of the question takes from the old question.title
  - Need to handle the case where `description` has a placeholder that needs to be replaced
  - Keep HTML formatting in `description` and `explanation`
  - If a question has no `single_choice_radio` or is empty, skip the question
  - The order of options must be sorted alphabetically (A, B, C, D...)

