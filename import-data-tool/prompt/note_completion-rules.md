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
