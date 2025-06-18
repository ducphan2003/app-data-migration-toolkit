### 2.2. SINGLE_SELECTION

- **Determine type**:

- Based on `type` in the old question

  - If it is "SINGLE-SELECTION" then create a new question_set with `question_type = "SINGLE_SELECTION"`
  - If it is `type = "FILL-IN-THE-BLANK"` and `question_type = "YES_NO"` then create a new question_set with `question_type = "SINGLE_SELECTION"`
  - If it is `type = "SINGLE-RADIO"` and `question_type = "TRUE_FALSE"` then create a new question_set with `question_type = "SINGLE_SELECTION"`
  - If it is `type = "SINGLE-SELECTION"` and `question_type = "TRUE_FALSE"` then create a new question_set with `question_type = "SINGLE_SELECTION"`
  - If it is `type = "SINGLE-SELECTION"` and `question_type = "YES_NO"` then create a new question_set with `question_type = "SINGLE_SELECTION"`
  - If it is `type = "SINGLE-SELECTION"` and `question_type = "OTHERS"` then create a new question_set with `question_type = "SINGLE_SELECTION"`
  - If it is `type = "SINGLE-SELECTION"` and `question_type = "MAP_DIAGRAM_LABEL"` then create a new question_set with `question_type = "SINGLE_SELECTION"`

- **Old structure**:

  ```json
  {
    "id": 1822,
    "quiz_id": 1714,
    "passage": 1,
    "title": "Part 1",
    "sort": 1,
    "time": null,
    "content": "<h3>READING PASSAGE 1</h3>\n<p>You should spend about 20 minutes on Questions 1 - 13 which are based on Reading Passage 1 below.</p>\n<h2>The Industrial Revolution in Britain</h2>\n<p>The Industrial Revolution began in Britain in the mid-1700s and by the 1830s and 1840s had spread to many other parts of the world, including the United States. In Britain, it was a period when a largely rural, agrarian society was transformed into an industrialised, urban one. Goods that had once been crafted by hand started to be produced in mass quantities by machines in factories, thanks to the invention of steam power and the introduction of new machines and manufacturing techniques in textiles, iron-making and other industries.</p>",
    "simplified_content": null,
    "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
    "date_created": "2024-07-14T07:25:51.875+07:00",
    "date_updated": "2024-09-10T18:22:31.896+07:00",
    "explanations": [],
    "questions": [
      {
        "id": 10868,
        "quiz_id": 0,
        "type": "SINGLE-SELECTION",
        "question_type": "TRUE_FALSE",
        "title": "",
        "status": "published",
        "content": "",
        "content_writing": "",
        "sort": 2,
        "order": 8,
        "part_id": 1822,
        "time_to_think": null,
        "listen_from": null,
        "locate": null,
        "explain": "<div>Bước 1: Hiểu câu hỏi: Mạng lưới kênh đào của Anh đã phát triển nhanh chóng để có thể vận chuyển nhiều hàng hóa hơn trong nước. Bước 2: Tìm các keywords được paraphrase trong bài: Britain's canals ~ canal network, carry goods ~ goods could be transported. Bước 3: So sánh và đối chiếu: Bài đọc đề cập đến việc \"tàu thuyền chạy bằng hơi nước được sử dụng rộng rãi để vận chuyển hàng hóa dọc theo các kênh đào của Anh\". Tuy nhiên, bài đọc không hề nhắc đến thông tin \"mạng lưới kênh đào phát triển nhanh chóng\". Bước 4: Đáp án: NOT GIVEN</div>",
        "description": "<h2>Questions 8 - 13:</h2>\n<p>Do the following statements agree with the information given in Reading Passage 1?</p>\n<p>In boxes 8-13 on your answer sheet, write</p>\n<p><strong>TRUE</strong> if the statement agrees with the information</p>\n<p><strong>FALSE</strong> if the statement contradicts the information</p>\n<p><strong>NOT GIVEN</strong> if there is no information on this</p>",
        "gap_fill_in_blank": null,
        "single_choice_radio": null,
        "selection": [
          {
            "text": "Britain's canal network grew rapidly so that more goods could be transported around the country.",
            "answer": "NOT GIVEN"
          }
        ],
        "mutilple_choice": null,
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
        "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
        "user_updated": "c2afe8a2-9330-4394-a11c-5a6c0d52d9d0",
        "date_created": "2024-07-14T07:25:51.925+07:00",
        "date_updated": "2024-08-24T22:37:09.96+07:00",
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
    "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
    "date_created": "2024-07-14T07:25:51.875+07:00",
    "date_updated": "2024-09-10T18:22:31.896+07:00",
    "title": "Part 1",
    "order": null,
    "content": "<h3>READING PASSAGE 1</h3>\n<p>You should spend about 20 minutes on Questions 1 - 13 which are based on Reading Passage 1 below.</p>\n<h2>The Industrial Revolution in Britain</h2>\n<p>The Industrial Revolution began in Britain in the mid-1700s and by the 1830s and 1840s had spread to many other parts of the world, including the United States. In Britain, it was a period when a largely rural, agrarian society was transformed into an industrialised, urban one. Goods that had once been crafted by hand started to be produced in mass quantities by machines in factories, thanks to the invention of steam power and the introduction of new machines and manufacturing techniques in textiles, iron-making and other industries.</p>",
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
        "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
        "date_created": "2024-07-14T07:25:51.925+07:00",
        "user_updated": "c2afe8a2-9330-4394-a11c-5a6c0d52d9d0",
        "date_updated": "2024-08-24T22:37:09.96+07:00",
        "question_type": "SINGLE_SELECTION",
        "question_count": 6,
        "title": "Questions 8-13",
        "description": "<h2>Questions 8 - 13:</h2>\n<p>Do the following statements agree with the information given in Reading Passage 1?</p>\n<p>In boxes 8-13 on your answer sheet, write</p>\n<p><strong>TRUE</strong> if the statement agrees with the information</p>\n<p><strong>FALSE</strong> if the statement contradicts the information</p>\n<p><strong>NOT GIVEN</strong> if there is no information on this</p>",
        "content": "",
        "option_title": "",
        "options": [
          {
            "text": "YES",
            "option": "TRUE"
          },
          {
            "text": "NO",
            "option": "FALSE"
          },
          {
            "text": "NOT GIVEN",
            "option": "NOT GIVEN"
          }
        ],
        "allow_reuse": false,
        "max_selections": 0,
        "sort": 2,
        "questions": [
          {
            "id": 1,
            "status": "published",
            "sort": 2,
            "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
            "date_created": "2024-07-14T07:25:51.925+07:00",
            "user_updated": "c2afe8a2-9330-4394-a11c-5a6c0d52d9d0",
            "date_updated": "2024-08-24T22:37:09.96+07:00",
            "title": "",
            "content": null,
            "locate": null,
            "order": 8,
            "explain": "<div>Bước 1: Hiểu câu hỏi: Mạng lưới kênh đào của Anh đã phát triển nhanh chóng để có thể vận chuyển nhiều hàng hóa hơn trong nước. Bước 2: Tìm các keywords được paraphrase trong bài: Britain's canals ~ canal network, carry goods ~ goods could be transported. Bước 3: So sánh và đối chiếu: Bài đọc đề cập đến việc \"tàu thuyền chạy bằng hơi nước được sử dụng rộng rãi để vận chuyển hàng hóa dọc theo các kênh đào của Anh\". Tuy nhiên, bài đọc không hề nhắc đến thông tin \"mạng lưới kênh đào phát triển nhanh chóng\". Bước 4: Đáp án: NOT GIVEN</div>",
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
            "text": "Britain's canal network grew rapidly so that more goods could be transported around the country.",
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
            "question_type": "TRUE_FALSE",
            "correct_answer": "NOT GIVEN",
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
     - `question_type`: Keep the old question.question_type
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
