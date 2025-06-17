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
