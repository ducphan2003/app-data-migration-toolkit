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
