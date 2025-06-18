### 2.6. SINGLE_CHOICE

- **Determine type**:

  - Based on `type` and `question_type` in the old question
  - If it is `type = "FILL-IN-THE_BLANK"` and `question_type = "MULTIPLE_CHOICE_ONE"` then create a new question_set with `question_type = "SINGLE_CHOICE"`
  - If it is `type = "SINGLE-RADIO"` and `question_type = "FILL_BLANK"` then create a new question_set with `question_type = "SINGLE_CHOICE"`
  - If it is `type = "SINGLE-RADIO"` and `question_type = "MULTIPLE_CHOICE_ONE"` then create a new question_set with `question_type = "SINGLE_CHOICE"`
  - If it is `type = "SINGLE-RADIO"` and `question_type = None` then create a new question_set with `question_type = "SINGLE_CHOICE"`
  - If it is `type = "SINGLE-SELECTION"` and `question_type = MULTIPLE_CHOICE_ONE` then create a new question_set with `question_type = "SINGLE_CHOICE"`

- **Old structure**:

  ```json
  {
    "id": 1825,
    "quiz_id": 1714,
    "passage": 3,
    "title": "Part 3",
    "sort": 3,
    "time": null,
    "content": "<h3>READING PASSAGE 3</h3>\n<p>You should spend about 20 minutes on Questions 38 - 40 which are based on Reading Passage 3 below.</p>\n<h2>Educational Excellence and Giftedness</h2>\n<p>Dr. Sarah Eyre's research on educational development has revealed important insights about how children achieve academic excellence. According to Eyre, traditional methods of identifying 'gifted' students often focus too heavily on standardized test scores and fail to recognize the potential in all children. She argues that with the right educational environment, most children can achieve standards typically associated with 'gifted' students. Eyre believes that the key lies not in strict discipline or rigid teaching methods, but in fostering a spirit of inquiry and encouraging students to question and explore. This approach, she suggests, helps develop critical thinking skills that are essential for academic success.</p>",
    "simplified_content": null,
    "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
    "date_created": "2024-07-14T07:34:53.822+07:00",
    "date_updated": "2024-09-10T18:22:31.987+07:00",
    "explanations": [],
    "questions": [
      {
        "id": 10883,
        "quiz_id": 0,
        "type": "SINGLE-RADIO",
        "question_type": "MULTIPLE_CHOICE_ONE",
        "title": "What does Eyre believe is needed for children to equal 'gifted' standards?",
        "status": "published",
        "content": "",
        "content_writing": "",
        "sort": 10,
        "order": 38,
        "part_id": 1825,
        "time_to_think": null,
        "listen_from": null,
        "locate": null,
        "explain": "<div>Bước 1: Hiểu và tìm keywords trong câu hỏi: \"What does Eyre believe is needed for children to equal 'gifted' standards?\" - Eyre tin rằng điều gì cần thiết để trẻ em đạt tiêu chuẩn 'năng khiếu'? Bước 2: Tìm thông tin trong đoạn văn: \"Eyre believes that the key lies not in strict discipline or rigid teaching methods, but in fostering a spirit of inquiry and encouraging students to question and explore.\" Bước 3: Phân tích các lựa chọn: A (strict discipline) bị loại vì bài nói \"not in strict discipline\", B đúng vì khớp với \"fostering a spirit of inquiry\". Bước 4: Đáp án: B</div>",
        "description": "<h2>Questions 38 - 40:</h2>\n<p>Choose the correct letter, A, B, C or D.</p>\n<p>Write the correct letter in boxes 38 - 40 on your answer sheet.</p>",
        "gap_fill_in_blank": null,
        "single_choice_radio": [
          {
            "text": "strict discipline from the teaching staff",
            "correct": false
          },
          {
            "text": "the development of a spirit of inquiry towards their studies",
            "correct": true
          },
          {
            "text": "higher standardized test scores",
            "correct": false
          },
          {
            "text": "more rigid teaching methods",
            "correct": false
          }
        ],
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
      },
      {
        "id": 10884,
        "quiz_id": 0,
        "type": "SINGLE-RADIO",
        "question_type": "MULTIPLE_CHOICE_ONE",
        "title": "According to the passage, traditional methods of identifying gifted students are criticized for:",
        "status": "published",
        "content": "",
        "content_writing": "",
        "sort": 11,
        "order": 39,
        "part_id": 1825,
        "time_to_think": null,
        "listen_from": null,
        "locate": null,
        "explain": "<div>Bước 1: Hiểu câu hỏi: \"According to the passage, traditional methods of identifying gifted students are criticized for:\" - Theo đoạn văn, các phương pháp truyền thống xác định học sinh năng khiếu bị chỉ trích vì điều gì? Bước 2: Tìm thông tin: \"traditional methods of identifying 'gifted' students often focus too heavily on standardized test scores and fail to recognize the potential in all children.\" Bước 3: Phân tích: focusing too heavily on test scores = over-relying on standardized testing. Bước 4: Đáp án: C</div>",
        "description": "<h2>Questions 38 - 40:</h2>\n<p>Choose the correct letter, A, B, C or D.</p>\n<p>Write the correct letter in boxes 38 - 40 on your answer sheet.</p>",
        "gap_fill_in_blank": null,
        "single_choice_radio": [
          {
            "text": "being too expensive to implement",
            "correct": false
          },
          {
            "text": "taking too much time to complete",
            "correct": false
          },
          {
            "text": "over-relying on standardized testing",
            "correct": true
          },
          {
            "text": "requiring too much teacher training",
            "correct": false
          }
        ],
        "selection": null,
        "mutilple_choice": null,
        "selection_option": null,
        "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
        "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
        "date_created": "2024-07-14T07:34:53.988+07:00",
        "date_updated": "2024-09-10T18:22:32.093+07:00",
        "instruction": null,
        "writing_logical_frame": null,
        "writing_graph_image": null,
        "writing_graph_description": null,
        "writing_graph_type": null,
        "time_limit": null,
        "audio_url": null,
        "min_words": 0,
        "max_words": 0
      },
      {
        "id": 10885,
        "quiz_id": 0,
        "type": "SINGLE-RADIO",
        "question_type": "MULTIPLE_CHOICE_ONE",
        "title": "The main purpose of Eyre's educational approach is to:",
        "status": "published",
        "content": "",
        "content_writing": "",
        "sort": 12,
        "order": 40,
        "part_id": 1825,
        "time_to_think": null,
        "listen_from": null,
        "locate": null,
        "explain": "<div>Bước 1: Hiểu câu hỏi: \"The main purpose of Eyre's educational approach is to:\" - Mục đích chính của phương pháp giáo dục của Eyre là gì? Bước 2: Tìm thông tin: \"This approach, she suggests, helps develop critical thinking skills that are essential for academic success.\" Bước 3: Phân tích: develop critical thinking skills = foster critical thinking abilities. Bước 4: Đáp án: D</div>",
        "description": "<h2>Questions 38 - 40:</h2>\n<p>Choose the correct letter, A, B, C or D.</p>\n<p>Write the correct letter in boxes 38 - 40 on your answer sheet.</p>",
        "gap_fill_in_blank": null,
        "single_choice_radio": [
          {
            "text": "increase test scores dramatically",
            "correct": false
          },
          {
            "text": "reduce the workload for teachers",
            "correct": false
          },
          {
            "text": "identify truly gifted students",
            "correct": false
          },
          {
            "text": "foster critical thinking abilities",
            "correct": true
          }
        ],
        "selection": null,
        "mutilple_choice": null,
        "selection_option": null,
        "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
        "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
        "date_created": "2024-07-14T07:34:53.999+07:00",
        "date_updated": "2024-09-10T18:22:32.105+07:00",
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
    "id": 1825,
    "sort": 3,
    "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
    "date_created": "2024-07-14T07:34:53.822+07:00",
    "date_updated": "2024-09-10T18:22:31.987+07:00",
    "title": "Part 3",
    "order": null,
    "content": "<h3>READING PASSAGE 3</h3>\n<p>You should spend about 20 minutes on Questions 38 - 40 which are based on Reading Passage 3 below.</p>\n<h2>Educational Excellence and Giftedness</h2>\n<p>Dr. Sarah Eyre's research on educational development has revealed important insights about how children achieve academic excellence. According to Eyre, traditional methods of identifying 'gifted' students often focus too heavily on standardized test scores and fail to recognize the potential in all children. She argues that with the right educational environment, most children can achieve standards typically associated with 'gifted' students. Eyre believes that the key lies not in strict discipline or rigid teaching methods, but in fostering a spirit of inquiry and encouraging students to question and explore. This approach, she suggests, helps develop critical thinking skills that are essential for academic success.</p>",
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
        "part_id": 1825,
        "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
        "date_created": "2024-07-14T07:34:53.97+07:00",
        "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
        "date_updated": "2024-09-10T18:22:32.105+07:00",
        "question_type": "SINGLE_CHOICE",
        "question_count": 3,
        "title": "Questions 38-40",
        "description": "<h2>Questions 38 - 40:</h2>\n<p>Choose the correct letter, A, B, C or D.</p>\n<p>Write the correct letter in boxes 38 - 40 on your answer sheet.</p>",
        "content": "",
        "option_title": "",
        "options": null,
        "allow_reuse": false,
        "max_selections": 0,
        "sort": 10,
        "questions": [
          {
            "id": 1,
            "status": "published",
            "sort": 10,
            "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
            "date_created": "2024-07-14T07:34:53.97+07:00",
            "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
            "date_updated": "2024-09-10T18:22:32.059+07:00",
            "title": null,
            "content": null,
            "locate": null,
            "order": 38,
            "explain": "<div>Bước 1: Hiểu và tìm keywords trong câu hỏi: \"What does Eyre believe is needed for children to equal 'gifted' standards?\" - Eyre tin rằng điều gì cần thiết để trẻ em đạt tiêu chuẩn 'năng khiếu'? Bước 2: Tìm thông tin trong đoạn văn: \"Eyre believes that the key lies not in strict discipline or rigid teaching methods, but in fostering a spirit of inquiry and encouraging students to question and explore.\" Bước 3: Phân tích các lựa chọn: A (strict discipline) bị loại vì bài nói \"not in strict discipline\", B đúng vì khớp với \"fostering a spirit of inquiry\". Bước 4: Đáp án: B</div>",
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
            "text": "What does Eyre believe is needed for children to equal 'gifted' standards?",
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
            "question_type": "SINGLE-CHOICE",
            "correct_answer": "B",
            "correct_answers": null,
            "options": [
              {
                "text": "strict discipline from the teaching staff",
                "option": "A",
                "is_correct": false
              },
              {
                "text": "the development of a spirit of inquiry towards their studies",
                "option": "B",
                "is_correct": true
              },
              {
                "text": "higher standardized test scores",
                "option": "C",
                "is_correct": false
              },
              {
                "text": "more rigid teaching methods",
                "option": "D",
                "is_correct": false
              }
            ]
          },
          {
            "id": 2,
            "status": "published",
            "sort": 11,
            "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
            "date_created": "2024-07-14T07:34:53.988+07:00",
            "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
            "date_updated": "2024-09-10T18:22:32.093+07:00",
            "title": null,
            "content": null,
            "locate": null,
            "order": 39,
            "explain": "<div>Bước 1: Hiểu câu hỏi: \"According to the passage, traditional methods of identifying gifted students are criticized for:\" - Theo đoạn văn, các phương pháp truyền thống xác định học sinh năng khiếu bị chỉ trích vì điều gì? Bước 2: Tìm thông tin: \"traditional methods of identifying 'gifted' students often focus too heavily on standardized test scores and fail to recognize the potential in all children.\" Bước 3: Phân tích: focusing too heavily on test scores = over-relying on standardized testing. Bước 4: Đáp án: C</div>",
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
            "text": "According to the passage, traditional methods of identifying gifted students are criticized for:",
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
            "question_type": "SINGLE-CHOICE",
            "correct_answer": "C",
            "correct_answers": null,
            "options": [
              {
                "text": "being too expensive to implement",
                "option": "A",
                "is_correct": false
              },
              {
                "text": "taking too much time to complete",
                "option": "B",
                "is_correct": false
              },
              {
                "text": "over-relying on standardized testing",
                "option": "C",
                "is_correct": true
              },
              {
                "text": "requiring too much teacher training",
                "option": "D",
                "is_correct": false
              }
            ]
          },
          {
            "id": 3,
            "status": "published",
            "sort": 12,
            "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
            "date_created": "2024-07-14T07:34:53.999+07:00",
            "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
            "date_updated": "2024-09-10T18:22:32.105+07:00",
            "title": null,
            "content": null,
            "locate": null,
            "order": 40,
            "explain": "<div>Bước 1: Hiểu câu hỏi: \"The main purpose of Eyre's educational approach is to:\" - Mục đích chính của phương pháp giáo dục của Eyre là gì? Bước 2: Tìm thông tin: \"This approach, she suggests, helps develop critical thinking skills that are essential for academic success.\" Bước 3: Phân tích: develop critical thinking skills = foster critical thinking abilities. Bước 4: Đáp án: D</div>",
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
            "text": "The main purpose of Eyre's educational approach is to:",
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
            "question_type": "SINGLE-CHOICE",
            "correct_answer": "D",
            "correct_answers": null,
            "options": [
              {
                "text": "increase test scores dramatically",
                "option": "A",
                "is_correct": false
              },
              {
                "text": "reduce the workload for teachers",
                "option": "B",
                "is_correct": false
              },
              {
                "text": "identify truly gifted students",
                "option": "C",
                "is_correct": false
              },
              {
                "text": "foster critical thinking abilities",
                "option": "D",
                "is_correct": true
              }
            ]
          }
        ]
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
