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
