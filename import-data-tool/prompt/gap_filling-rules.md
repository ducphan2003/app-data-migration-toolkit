### 2.1. GAP_FILLING

- **Determine type**:

  - Based on `question_type` in the old question
  - If it is `type = "FILL-IN-THE-BLANK"` and `question_type = "FILL_BLANK"` then create a new question_set with `question_type = "GAP_FILLING"`
  - If it is `type = "FILL-IN-THE-BLANK"` and `question_type = "MAP_DIAGRAM_LABEL"` then create a new question_set with `question_type = "GAP_FILLING"`
  - If it is `type = "FILL-IN-THE-BLANK"` and `question_type = "OTHERS"` then create a new question_set with `question_type = "GAP_FILLING"`
  - If it is `type = "MULTIPLE"` and `question_type = "FILL_BLANK"` then create a new question_set with `question_type = "GAP_FILLING"`
  - If it is `type = "SINGLE-SELECTION"` and `question_type = "MATCHING_HEADING"` then create a new question_set with `question_type = "MATCHING"`

- **Old structure**:

  ```json
  {
    "id": 1822,
    "quiz_id": 1714,
    "passage": 1,
    "title": "Part 1",
    "sort": 1,
    "time": null,
    "content": "<h3>READING PASSAGE 1</h3>\n<p>You should spend about 20 minutes on Questions 1 - 2 which are based on Reading Passage 1 below.</p>\n<h2>Climate Change and Agriculture</h2>\n<p>Climate change is having a significant impact on agriculture worldwide. Rising temperatures and changing precipitation patterns are affecting crop yields in many regions. Farmers are adapting by developing new {[techniques][1]} to manage water resources more efficiently. Additionally, scientists are working on creating drought-resistant varieties of crops to help farmers cope with the changing climate. The development of these new {[technologies][2]} is crucial for ensuring food security in the future.</p>",
    "simplified_content": null,
    "user_created": "user_created",
    "date_created": "date_created",
    "date_updated": "date_updated",
    "explanations": [],
    "questions": [
      {
        "id": 10867,
        "quiz_id": 0,
        "type": "FILL-IN-THE-BLANK",
        "question_type": "FILL_BLANK",
        "title": "Complete the notes below. Choose ONE WORD ONLY from the passage for each answer. Write your answers in boxes 1-2 on your answer sheet.",
        "status": "published",
        "content": "",
        "content_writing": "",
        "sort": 1,
        "order": 1,
        "part_id": 1822,
        "time_to_think": null,
        "listen_from": null,
        "locate": null,
        "explain": "<div><strong>Câu 1:</strong> Bước 1: Hiểu câu hỏi - Farmers are developing new _______ to manage water resources. Bước 2: Xác định loại từ - NOUN (new + NOUN). Bước 3: Tìm keywords trong bài - developing new techniques to manage water resources. Bước 4: Đáp án: techniques</div>\n<div><strong>Câu 2:</strong> Bước 1: Hiểu câu hỏi - The development of new _______ is crucial for food security. Bước 2: Xác định loại từ - NOUN (new + NOUN). Bước 3: Tìm keywords trong bài - development of these new technologies. Bước 4: Đáp án: technologies</div>",
        "description": "<h2>Questions 1 - 2:</h2>",
        "gap_fill_in_blank": "<h3>Climate Change and Agriculture</h3>\n<table border=\"1\">\n<tbody>\n<tr>\n<td>\n<h4><strong>Impact on Farming</strong></h4>\n<p>• Farmers are developing new {[techniques][1]} to manage water resources efficiently.</p>\n<p>• The development of new {[technologies][2]} is crucial for ensuring food security.</p>\n</td>\n</tr>\n</tbody>\n</table>",
        "single_choice_radio": null,
        "selection": null,
        "mutilple_choice": null,
        "selection_option": null,
        "user_created": "user_created",
        "user_updated": "user_updated",
        "date_created": "date_created",
        "date_updated": "date_updated",
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
    "id": 1822,
    "sort": 1,
    "user_created": "user_created",
    "date_created": "date_created",
    "date_updated": "date_updated",
    "title": "Part 1",
    "order": null,
    "content": "<h3>READING PASSAGE 1</h3>\n<p>You should spend about 20 minutes on Questions 1 - 2 which are based on Reading Passage 1 below.</p>\n<h2>Climate Change and Agriculture</h2>\n<p>Climate change is having a significant impact on agriculture worldwide. Rising temperatures and changing precipitation patterns are affecting crop yields in many regions. Farmers are adapting by developing new techniques to manage water resources more efficiently. Additionally, scientists are working on creating drought-resistant varieties of crops to help farmers cope with the changing climate. The development of these new technologies is crucial for ensuring food security in the future.</p>",
    "quiz": 1714,
    "time": null,
    "passage": 1,
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
        "part_id": 1822,
        "user_created": "user_created",
        "date_created": "date_created",
        "user_updated": "user_updated",
        "date_updated": "date_updated",
        "question_type": "GAP_FILLING",
        "question_count": 2,
        "title": "Questions 1-2",
        "description": "Complete the notes below. Choose ONE WORD ONLY from the passage for each answer. Write your answers in boxes 1-2 on your answer sheet.",
        "content": "<h3>Climate Change and Agriculture</h3>\n<table border=\"1\">\n<tbody>\n<tr>\n<td>\n<h4><strong>Impact on Farming</strong></h4>\n<p>• Farmers are developing new ______ to manage water resources efficiently.</p>\n<p>• The development of new ______ is crucial for ensuring food security.</p>\n</td>\n</tr>\n</tbody>\n</table>",
        "option_title": null,
        "options": null,
        "allow_reuse": null,
        "max_selections": null,
        "sort": 1,
        "questions": [
          {
            "id": 1,
            "status": "published",
            "sort": 1,
            "user_created": "user_created",
            "date_created": "date_created",
            "user_updated": "user_updated",
            "date_updated": "date_updated",
            "title": "",
            "content": null,
            "locate": null,
            "order": 1,
            "explain": "<div><strong>Câu 1:</strong> Bước 1: Hiểu câu hỏi - Farmers are developing new _______ to manage water resources. Bước 2: Xác định loại từ - NOUN (new + NOUN). Bước 3: Tìm keywords trong bài - developing new techniques to manage water resources. Bước 4: Đáp án: techniques</div>",
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
            "text": null,
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
            "correct_answer": null,
            "correct_answers": ["techniques"],
            "options": null
          },
          {
            "id": 2,
            "status": "published",
            "sort": 2,
            "user_created": "user_created",
            "date_created": "date_created",
            "user_updated": "user_updated",
            "date_updated": "date_updated",
            "title": "",
            "content": null,
            "locate": null,
            "order": 2,
            "explain": "<div><strong>Câu 2:</strong> Bước 1: Hiểu câu hỏi - The development of new _______ is crucial for food security. Bước 2: Xác định loại từ - NOUN (new + NOUN). Bước 3: Tìm keywords trong bài - development of these new technologies. Bước 4: Đáp án: technologies</div>",
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
            "text": null,
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
            "correct_answer": null,
            "correct_answers": ["technologies"],
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
     - `question_type`: Keep the old question.question_type
     - `correct_answers`:
       - Take the answer from the old `{[answer][number]}` in the `gap_fill_in_blank`
       - Always in array format: ["answer1", "answer2"]
       - If answer contains multiple options like "labour | labor", split into ["labour", "labor"]
       - NEVER use string format like "labour | labor" in the array
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
