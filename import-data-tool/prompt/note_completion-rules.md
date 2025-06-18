### 2.5. NOTE_COMPLETION

- **Determine type**:

  - Based on `type` and `question_type` in the old question
  - If it is `type = "FILL-IN-THE-BLANK"` and `question_type = "FILL_BLANK"` and has `gap_fill_in_blank` containing the vocabulary list then create a new question_set with `question_type = "NOTE_COMPLETION"`
  - If it is `type = "FILL-IN-THE-BLANK"` and `question_type = "MATCHING_NAMES"` then create a new question_set with `question_type = "NOTE_COMPLETION"`
  - If it is `type = "FILL-IN-THE-BLANK"` and `question_type = "MATCHING_INFO"` then create a new question_set with `question_type = "NOTE_COMPLETION"`
  - If it is `type = "SINGLE-SELECTION"` and `question_type = "MATCHING_NAMES"` then create a new question_set with `question_type = "NOTE_COMPLETION"`
  - If it is `type = "SINGLE-SELECTION"` and `question_type = "MATCHING_INFO"` then create a new question_set with `question_type = "NOTE_COMPLETION"`

- **Old structure**:

  ```json
  {
    "id": 1824,
    "quiz_id": 1714,
    "passage": 3,
    "title": "Part 3",
    "sort": 3,
    "time": null,
    "content": "<h3>READING PASSAGE 3</h3>\n<p>You should spend about 20 minutes on Questions 27 - 32 which are based on Reading Passage 3 below.</p>\n<h2>Maryam Mirzakhani: A Mathematical Pioneer</h2>\n<p>Maryam Mirzakhani was an Iranian mathematician who made groundbreaking contributions to the field of mathematics. Born in 1977, she was the first woman to receive the Fields Medal, often considered the Nobel Prize of mathematics. Her work on hyperbolic geometry and dynamical systems has influenced countless researchers in the field. Despite facing numerous challenges as a woman in mathematics, she remained determined and passionate about her research until her death in 2017.</p>",
    "simplified_content": null,
    "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
    "date_created": "2024-07-14T07:34:53.822+07:00",
    "date_updated": "2024-09-10T18:22:31.987+07:00",
    "explanations": [],
    "questions": [
      {
        "id": 10882,
        "quiz_id": 0,
        "type": "FILL-IN-THE-BLANK",
        "question_type": "FILL_BLANK",
        "title": "Complete the summary using the list of phrases, A-K, below. Write the correct letter, A-K, in boxes 27-32 on your answer sheet.",
        "status": "published",
        "content": "",
        "content_writing": "",
        "sort": 9,
        "order": 27,
        "part_id": 1824,
        "time_to_think": null,
        "listen_from": null,
        "locate": null,
        "explain": "<div><strong>Câu 27:</strong> Bước 1: Hiểu câu hỏi - Maryam Mirzakhani is regarded as _______ in mathematics. Bước 2: Tìm keywords trong đoạn văn - \"first woman to receive the Fields Medal\". Bước 3: Paraphrase - \"first woman\" tương đương với \"pioneer\". Bước 4: Đáp án: H (a pioneer)</div>\n<div><strong>Câu 28:</strong> Bước 1: Hiểu câu hỏi - Her research focused on _______ and dynamical systems. Bước 2: Tìm keywords trong đoạn văn - \"work on hyperbolic geometry and dynamical systems\". Bước 3: So sánh với danh sách từ vựng. Bước 4: Đáp án: C (hyperbolic geometry)</div>\n<div><strong>Câu 29:</strong> Bước 1: Hiểu câu hỏi - She received the _______ in recognition of her work. Bước 2: Tìm keywords trong đoạn văn - \"first woman to receive the Fields Medal\". Bước 3: So sánh với danh sách từ vựng. Bước 4: Đáp án: F (Fields Medal)</div>\n<div><strong>Câu 30:</strong> Bước 1: Hiểu câu hỏi - Her nationality was _______. Bước 2: Tìm keywords trong đoạn văn - \"Iranian mathematician\". Bước 3: So sánh với danh sách từ vựng. Bước 4: Đáp án: A (Iranian)</div>\n<div><strong>Câu 31:</strong> Bước 1: Hiểu câu hỏi - She remained _______ despite facing challenges. Bước 2: Tìm keywords trong đoạn văn - \"she remained determined and passionate\". Bước 3: So sánh với danh sách từ vựng. Bước 4: Đáp án: B (determined)</div>\n<div><strong>Câu 32:</strong> Bước 1: Hiểu câu hỏi - Her work has _______ many researchers. Bước 2: Tìm keywords trong đoạn văn - \"has influenced countless researchers\". Bước 3: So sánh với danh sách từ vựng. Bước 4: Đáp án: D (influenced)</div>",
        "description": "<h2>Questions 27 - 32:</h2>",
        "gap_fill_in_blank": "<h3><strong>List of words</strong></h3>\n<table border=\"1\">\n<tbody>\n<tr>\n<td><strong>A</strong> Iranian</td>\n<td><strong>B</strong> determined</td>\n<td><strong>C</strong> hyperbolic geometry</td>\n</tr>\n<tr>\n<td><strong>D</strong> influenced</td>\n<td><strong>E</strong> challenges</td>\n<td><strong>F</strong> Fields Medal</td>\n</tr>\n<tr>\n<td><strong>G</strong> passionate</td>\n<td><strong>H</strong> a pioneer</td>\n<td><strong>I</strong> research</td>\n</tr>\n<tr>\n<td><strong>J</strong> contributions</td>\n<td><strong>K</strong> groundbreaking</td>\n<td></td>\n</tr>\n</tbody>\n</table>\n\n<h3><strong>Notes on Maryam Mirzakhani</strong></h3>\n<table border=\"1\">\n<tbody>\n<tr>\n<td>\n<h4><strong>Personal Background</strong></h4>\n<p>• Maryam Mirzakhani is regarded as {[H][27]} in the field of mathematics.</p>\n<p>• Her nationality was {[A][30]} and she was born in 1977.</p>\n<h4><strong>Academic Achievements</strong></h4>\n<p>• Her research focused on {[C][28]} and dynamical systems.</p>\n<p>• She received the {[F][29]} in recognition of her work.</p>\n<p>• Her work has {[D][32]} countless researchers in the field.</p>\n<h4><strong>Personal Qualities</strong></h4>\n<p>• Despite facing numerous challenges, she remained {[B][31]} and passionate about her research.</p>\n</td>\n</tr>\n</tbody>\n</table>",
        "single_choice_radio": null,
        "selection": null,
        "mutilple_choice": null,
        "selection_option": null,
        "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
        "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
        "date_created": "2024-07-14T07:34:53.97+07:00",
        "date_updated": "2024-09-10T18:22:32.059+07:00",
        "instruction": null,
        "writing_logical_frame": null,
        "writing_graph_image": null,
        "writing_graph_description": null,
        "writing_graph_type": null,
        "time_limit": null,
        "audio_url": null,
        "min_words": 0,
        "max_words": 0
      }
    ],
    "vocabs": [],
    "listen_from": null,
    "listen_to": null,
    "instruction": null
  }
  ```

- **New structure**:

  ```json
  {
    "id": 1824,
    "sort": 3,
    "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
    "date_created": "2024-07-14T07:34:53.822+07:00",
    "date_updated": "2024-09-10T18:22:31.987+07:00",
    "title": "Part 3",
    "order": null,
    "content": "<h3>READING PASSAGE 3</h3>\n<p>You should spend about 20 minutes on Questions 27 - 32 which are based on Reading Passage 3 below.</p>\n<h2>Maryam Mirzakhani: A Mathematical Pioneer</h2>\n<p>Maryam Mirzakhani was an Iranian mathematician who made groundbreaking contributions to the field of mathematics. Born in 1977, she was the first woman to receive the Fields Medal, often considered the Nobel Prize of mathematics. Her work on hyperbolic geometry and dynamical systems has influenced countless researchers in the field. Despite facing numerous challenges as a woman in mathematics, she remained determined and passionate about her research until her death in 2017.</p>",
    "quiz": 1714,
    "time": null,
    "passage": 3,
    "simplified_content": null,
    "question_count": 0,
    "listen_from": null,
    "listen_to": null,
    "instruction": null,
    "task_instruction": null,
    "transcription": null,
    "file_id": null,
    "question_sets": [
      {
        "id": 1,
        "part_id": 1824,
        "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
        "date_created": "2024-07-14T07:34:53.97+07:00",
        "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
        "date_updated": "2024-09-10T18:22:32.059+07:00",
        "question_type": "NOTE_COMPLETION",
        "question_count": 6,
        "title": "Questions 27-32",
        "description": "Complete the summary using the list of phrases, A-K, below. Write the correct letter, A-K, in boxes 27-32 on your answer sheet.",
        "content": "<h3><strong>Notes on Maryam Mirzakhani</strong></h3>\n<div class=\"note-completion-content\">\n<table border=\"1\">\n<tbody>\n<tr>\n<td>\n<h4><strong>Personal Background</strong></h4>\n<p>• Maryam Mirzakhani is regarded as <span class=\"gap-placeholder\" data-question-id=\"note_comp_27\">______</span> in the field of mathematics.</p>\n<p>• Her nationality was <span class=\"gap-placeholder\" data-question-id=\"note_comp_30\">______</span> and she was born in 1977.</p>\n<h4><strong>Academic Achievements</strong></h4>\n<p>• Her research focused on <span class=\"gap-placeholder\" data-question-id=\"note_comp_28\">______</span> and dynamical systems.</p>\n<p>• She received the <span class=\"gap-placeholder\" data-question-id=\"note_comp_29\">______</span> in recognition of her work.</p>\n<p>• Her work has <span class=\"gap-placeholder\" data-question-id=\"note_comp_32\">______</span> countless researchers in the field.</p>\n<h4><strong>Personal Qualities</strong></h4>\n<p>• Despite facing numerous challenges, she remained <span class=\"gap-placeholder\" data-question-id=\"note_comp_31\">______</span> and passionate about her research.</p>\n</td>\n</tr>\n</tbody>\n</table>\n</div>",
        "option_title": "",
        "options": [
          {
            "text": "Iranian",
            "option": "A"
          },
          {
            "text": "determined",
            "option": "B"
          },
          {
            "text": "hyperbolic geometry",
            "option": "C"
          },
          {
            "text": "influenced",
            "option": "D"
          },
          {
            "text": "challenges",
            "option": "E"
          },
          {
            "text": "Fields Medal",
            "option": "F"
          },
          {
            "text": "passionate",
            "option": "G"
          },
          {
            "text": "a pioneer",
            "option": "H"
          },
          {
            "text": "research",
            "option": "I"
          },
          {
            "text": "contributions",
            "option": "J"
          },
          {
            "text": "groundbreaking",
            "option": "K"
          }
        ],
        "allow_reuse": true,
        "max_selections": 0,
        "sort": 9,
        "questions": [
          {
            "id": 1,
            "status": "published",
            "sort": 9,
            "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
            "date_created": "2024-07-14T07:34:53.97+07:00",
            "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
            "date_updated": "2024-09-10T18:22:32.059+07:00",
            "title": "",
            "content": null,
            "locate": null,
            "order": 27,
            "explain": "<div><strong>Câu 27:</strong> Bước 1: Hiểu câu hỏi - Maryam Mirzakhani is regarded as _______ in mathematics. Bước 2: Tìm keywords trong đoạn văn - \"first woman to receive the Fields Medal\". Bước 3: Paraphrase - \"first woman\" tương đương với \"pioneer\". Bước 4: Đáp án: H (a pioneer)</div>",
            "description": null,
            "content_writing": null,
            "time_to_think": null,
            "listen_from": null,
            "instruction": null,
            "writing_graph_image": null,
            "writing_graph_description": null,
            "writing_graph_type": null,
            "audio_url": null,
            "time_limit": 30,
            "max_words": null,
            "min_words": null,
            "text": "",
            "locate_info": null,
            "quiz_id": 0,
            "part_id": null,
            "type": "",
            "gap_fill_in_blank": null,
            "single_choice_radio": null,
            "selection": null,
            "mutilple_choice": null,
            "selection_option": null,
            "question_set_id": 1,
            "question_type": "FILL_BLANK",
            "correct_answer": "H",
            "correct_answers": null,
            "options": null
          },
          {
            "id": 2,
            "status": "published",
            "sort": 9,
            "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
            "date_created": "2024-07-14T07:34:53.97+07:00",
            "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
            "date_updated": "2024-09-10T18:22:32.059+07:00",
            "title": "",
            "content": null,
            "locate": null,
            "order": 28,
            "explain": "<div><strong>Câu 28:</strong> Bước 1: Hiểu câu hỏi - Her research focused on _______ and dynamical systems. Bước 2: Tìm keywords trong đoạn văn - \"work on hyperbolic geometry and dynamical systems\". Bước 3: So sánh với danh sách từ vựng. Bước 4: Đáp án: C (hyperbolic geometry)</div>",
            "description": null,
            "content_writing": null,
            "time_to_think": null,
            "listen_from": null,
            "instruction": null,
            "writing_graph_image": null,
            "writing_graph_description": null,
            "writing_graph_type": null,
            "audio_url": null,
            "time_limit": 30,
            "max_words": null,
            "min_words": null,
            "text": "",
            "locate_info": null,
            "quiz_id": 0,
            "part_id": null,
            "type": "",
            "gap_fill_in_blank": null,
            "single_choice_radio": null,
            "selection": null,
            "mutilple_choice": null,
            "selection_option": null,
            "question_set_id": 1,
            "question_type": "FILL_BLANK",
            "correct_answer": "C",
            "correct_answers": null,
            "options": null
          },
          {
            "id": 3,
            "status": "published",
            "sort": 9,
            "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
            "date_created": "2024-07-14T07:34:53.97+07:00",
            "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
            "date_updated": "2024-09-10T18:22:32.059+07:00",
            "title": "",
            "content": null,
            "locate": null,
            "order": 29,
            "explain": "<div><strong>Câu 29:</strong> Bước 1: Hiểu câu hỏi - She received the _______ in recognition of her work. Bước 2: Tìm keywords trong đoạn văn - \"first woman to receive the Fields Medal\". Bước 3: So sánh với danh sách từ vựng. Bước 4: Đáp án: F (Fields Medal)</div>",
            "description": null,
            "content_writing": null,
            "time_to_think": null,
            "listen_from": null,
            "instruction": null,
            "writing_graph_image": null,
            "writing_graph_description": null,
            "writing_graph_type": null,
            "audio_url": null,
            "time_limit": 30,
            "max_words": null,
            "min_words": null,
            "text": "",
            "locate_info": null,
            "quiz_id": 0,
            "part_id": null,
            "type": "",
            "gap_fill_in_blank": null,
            "single_choice_radio": null,
            "selection": null,
            "mutilple_choice": null,
            "selection_option": null,
            "question_set_id": 1,
            "question_type": "FILL_BLANK",
            "correct_answer": "F",
            "correct_answers": null,
            "options": null
          },
          {
            "id": 4,
            "status": "published",
            "sort": 9,
            "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
            "date_created": "2024-07-14T07:34:53.97+07:00",
            "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
            "date_updated": "2024-09-10T18:22:32.059+07:00",
            "title": "",
            "content": null,
            "locate": null,
            "order": 30,
            "explain": "<div><strong>Câu 30:</strong> Bước 1: Hiểu câu hỏi - Her nationality was _______. Bước 2: Tìm keywords trong đoạn văn - \"Iranian mathematician\". Bước 3: So sánh với danh sách từ vựng. Bước 4: Đáp án: A (Iranian)</div>",
            "description": null,
            "content_writing": null,
            "time_to_think": null,
            "listen_from": null,
            "instruction": null,
            "writing_graph_image": null,
            "writing_graph_description": null,
            "writing_graph_type": null,
            "audio_url": null,
            "time_limit": 30,
            "max_words": null,
            "min_words": null,
            "text": "",
            "locate_info": null,
            "quiz_id": 0,
            "part_id": null,
            "type": "",
            "gap_fill_in_blank": null,
            "single_choice_radio": null,
            "selection": null,
            "mutilple_choice": null,
            "selection_option": null,
            "question_set_id": 1,
            "question_type": "FILL_BLANK",
            "correct_answer": "A",
            "correct_answers": null,
            "options": null
          },
          {
            "id": 5,
            "status": "published",
            "sort": 9,
            "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
            "date_created": "2024-07-14T07:34:53.97+07:00",
            "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
            "date_updated": "2024-09-10T18:22:32.059+07:00",
            "title": "",
            "content": null,
            "locate": null,
            "order": 31,
            "explain": "<div><strong>Câu 31:</strong> Bước 1: Hiểu câu hỏi - She remained _______ despite facing challenges. Bước 2: Tìm keywords trong đoạn văn - \"she remained determined and passionate\". Bước 3: So sánh với danh sách từ vựng. Bước 4: Đáp án: B (determined)</div>",
            "description": null,
            "content_writing": null,
            "time_to_think": null,
            "listen_from": null,
            "instruction": null,
            "writing_graph_image": null,
            "writing_graph_description": null,
            "writing_graph_type": null,
            "audio_url": null,
            "time_limit": 30,
            "max_words": null,
            "min_words": null,
            "text": "",
            "locate_info": null,
            "quiz_id": 0,
            "part_id": null,
            "type": "",
            "gap_fill_in_blank": null,
            "single_choice_radio": null,
            "selection": null,
            "mutilple_choice": null,
            "selection_option": null,
            "question_set_id": 1,
            "question_type": "FILL_BLANK",
            "correct_answer": "B",
            "correct_answers": null,
            "options": null
          },
          {
            "id": 6,
            "status": "published",
            "sort": 9,
            "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
            "date_created": "2024-07-14T07:34:53.97+07:00",
            "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
            "date_updated": "2024-09-10T18:22:32.059+07:00",
            "title": "",
            "content": null,
            "locate": null,
            "order": 32,
            "explain": "<div><strong>Câu 32:</strong> Bước 1: Hiểu câu hỏi - Her work has _______ many researchers. Bước 2: Tìm keywords trong đoạn văn - \"has influenced countless researchers\". Bước 3: So sánh với danh sách từ vựng. Bước 4: Đáp án: D (influenced)</div>",
            "description": null,
            "content_writing": null,
            "time_to_think": null,
            "listen_from": null,
            "instruction": null,
            "writing_graph_image": null,
            "writing_graph_description": null,
            "writing_graph_type": null,
            "audio_url": null,
            "time_limit": 30,
            "max_words": null,
            "min_words": null,
            "text": "",
            "locate_info": null,
            "quiz_id": 0,
            "part_id": null,
            "type": "",
            "gap_fill_in_blank": null,
            "single_choice_radio": null,
            "selection": null,
            "mutilple_choice": null,
            "selection_option": null,
            "question_set_id": 1,
            "question_type": "FILL_BLANK",
            "correct_answer": "D",
            "correct_answers": null,
            "options": null
          }
        ]
      }
    ]
  }
  ```

- **Migration rules**:

  1. **Question Set**:

     - `part_id`: Take from the current part
     - `question_type`: Set = old question.question_type
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
     - `question_type`: Keep the old question.question_type
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
