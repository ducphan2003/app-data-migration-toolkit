### 2.4. MULTIPLE_CHOICE_MANY

- **Determine type**:

  - Based on `type` and `question_type` in the old question
  - If it is `type = "MULTIPLE"` and `question_type = "MULTIPLE_CHOICE_MANY"` then create a new question_set with `question_type = "MULTIPLE_CHOICE_MANY"`
  - If it is `type = "MULTIPLE"` and `question_type = None` then create a new question_set with `question_type = "MULTIPLE_CHOICE_MANY"`

- **Old structure**:

  ```json
  {
    "id": 1823,
    "quiz_id": 1714,
    "passage": 2,
    "title": "Part 2",
    "sort": 2,
    "time": null,
    "content": "<h3>READING PASSAGE 2</h3>\n<p>Shortened passage content...</p>",
    "simplified_content": null,
    "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
    "date_created": "2024-07-14T07:34:53.822+07:00",
    "date_updated": "2024-09-10T18:22:31.987+07:00",
    "explanations": [],
    "questions": [
      {
        "id": 10880,
        "quiz_id": 0,
        "type": "MULTIPLE",
        "question_type": "MULTIPLE_CHOICE_MANY",
        "title": "Shortened Question Title Here",
        "status": "published",
        "content": "",
        "content_writing": "",
        "sort": 7,
        "order": 23,
        "part_id": 1823,
        "time_to_think": null,
        "listen_from": null,
        "locate": null,
        "explain": null,
        "description": "<h2><span class=\"fontstyle0\">Questions 23 - 24:</span></h2>\n<p><span class=\"fontstyle0\">Choose </span><span class=\"fontstyle2\">TWO </span><span class=\"fontstyle0\">letters, </span><span class=\"fontstyle2\"><strong>A-E</strong>. </span></p>\n<p><span class=\"fontstyle0\">Write the correct letters in boxes 23 - 24 on your answer sheet.</span></p>",
        "gap_fill_in_blank": null,
        "single_choice_radio": null,
        "selection": null,
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
            "explain": "<div>Shortened explanation for option 2...</div>"
          },
          {
            "text": "aspects of the Wimbledon tournament which increased her stress levels",
            "correct": true,
            "order": 4,
            "explain": "<div>Shortened explanation for option 4...</div>"
          }
        ],
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
    "id": 1823,
    "sort": 2,
    "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
    "date_created": "2024-07-14T07:34:53.822+07:00",
    "date_updated": "2024-09-10T18:22:31.987+07:00",
    "title": "Part 2",
    "order": null,
    "content": "<h3>READING PASSAGE 2</h3>\n<p>Shortened passage content...</p>",
    "quiz": 1714,
    "time": null,
    "passage": 2,
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
        "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
        "date_created": "2024-07-14T07:34:53.97+07:00",
        "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
        "date_updated": "2024-09-10T18:22:32.059+07:00",
        "sort": 1,
        "part_id": 1823,
        "question_type": "MULTIPLE_CHOICE_MANY",
        "question_count": 2,
        "title": "Questions 23-24",
        "description": "<h2><span class=\"fontstyle0\">Questions 23 - 24:</span></h2>\n<p><span class=\"fontstyle0\">Choose </span><span class=\"fontstyle2\">TWO </span><span class=\"fontstyle0\">letters, </span><span class=\"fontstyle2\"><strong>A-E</strong>. </span></p>\n<p><span class=\"fontstyle0\">Write the correct letters in boxes 23 - 24 on your answer sheet.</span></p>",
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
          },
          {
            "text": "measures which she had taken to manage her stress levels",
            "option": "C"
          },
          {
            "text": "aspects of the Wimbledon tournament which increased her stress levels",
            "option": "D"
          },
          {
            "text": "reactions to her social media posts about her experience at Wimbledon",
            "option": "E"
          }
        ],
        "allow_reuse": false,
        "max_selections": 2,
        "questions": [
          {
            "id": 1,
            "status": "published",
            "sort": 1,
            "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
            "date_created": "2024-07-14T07:34:53.97+07:00",
            "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
            "date_updated": "2024-09-10T18:22:32.059+07:00",
            "title": "",
            "content": "",
            "locate": null,
            "order": null,
            "explain": "<div>Shortened explanation for option 2...</div>",
            "description": null,
            "content_writing": "",
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
            "question_type": "MULTIPLE",
            "correct_answer": "",
            "correct_answers": ["B", "D"],
            "options": null,
            "explanation": null
          },
          {
            "id": 1,
            "status": "published",
            "sort": 2,
            "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
            "date_created": "2024-07-14T07:34:53.97+07:00",
            "user_updated": "266f2058-72cc-4c10-9f12-dbc5045539bf",
            "date_updated": "2024-09-10T18:22:32.059+07:00",
            "title": "",
            "content": "",
            "locate": null,
            "order": null,
            "explain": "<div>Shortened explanation for option 4...</div>",
            "description": null,
            "content_writing": "",
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
            "question_type": "MULTIPLE",
            "correct_answer": "",
            "correct_answers": ["B", "D"],
            "options": null,
            "explanation": null
          }
        ]
      }
    ]
  }
  ```

- **Migration rules**:

  1. **Question Set**:

     - `part_id`: Take from the current part
     - `question_type`: Set = "MULTIPLE_CHOICE_MANY"
     - `question_count`: Count the number of correct answers in the old question.mutilple_choice (number of options with `correct = true`)
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
     - **IMPORTANT**: Create multiple questions - one for each correct answer in the old question.mutilple_choice
     - Number of questions = Number of options with `correct = true`
     - For each question:
       - `question_type`: Set = "MULTIPLE"
       - `sort`: Sequential numbering (1, 2, 3...)
       - `correct_answers`:
         - Take ALL options with `correct = true` from the old question.mutilple_choice
         - Convert to an array of letters corresponding to (A, B, C...)
         - Example: if option 2 and 4 are correct → ["B", "D"]
         - **All questions share the same correct_answers array**
       - `text`: Set = "" (because the text is in the title of the question_set)
       - `explain`:
         - Each question gets the explanation from its corresponding correct option
         - Question 1: explanation from the 1st correct option
         - Question 2: explanation from the 2nd correct option
         - If no explanation in option, use the old question.explain
       - Other fields:
         - `quiz_id`: Set = 0
         - `type`: Set = ""
         - `part_id`: Set = null
         - `correct_answer`: Set = ""
         - `options`: Set = null
         - `title`: Set = ""
         - `content`: Set = ""

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
