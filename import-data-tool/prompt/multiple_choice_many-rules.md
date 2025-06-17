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
