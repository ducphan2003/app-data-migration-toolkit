# Rules for defining IELTS data structure and transformation

## 1. Migration rules by object

### 1.1. Quiz

- **Fields to migrate**:
  - `id`: Keep as is
  - `status`: Keep as is (default 'draft')
  - `sort`: Keep as is
  - `user_created`: Keep as is
  - `date_created`: Keep as is
  - `user_updated`: Keep as is
  - `date_updated`: Keep as is
  - `type`: Keep as is
  - `content`: Keep as is
  - `title`: Keep as is
  - `order`: Keep as is
  - `time`: Keep as is
  - `description`: Keep as is
  - `instruction`: Keep as is
  - `quiz_code`: Keep as is
  - `limit_submit`: Keep as is
  - `question`: Keep as is
  - `samples`: Keep as is
  - `thumbnail`: Keep as is
  - `quiz_type`: Keep as is
  - `full_id`: Keep as is
  - `is_test`: Keep as is
  - `mode`: Keep as is (default 0)
  - `simplified_id`: Keep as is
  - `mock_test_id`: Keep as is
  - `mock_test_type`: Keep as is
  - `short_description`: Keep as is
  - `practice_listing_priority`: Keep as is (default 0)
  - `is_public`: Keep as is (default true)
  - `writing_task_type`: Keep as is
  - `meta`: Keep as is
  - `prompt_set_id`: Keep as is
  - `speaking_part_type`: Keep as is
  - `speaking_topic_id`: Keep as is
- **Fields to set specific values**:
  - `vote_count`: Set = 0
  - `total_submitted`: Set = 0
- **Fields to skip**:
  - `listening`: Skip, will be transferred to `part.file_id`
  - `instruction_audio`: Skip, will be added later

### 1.2. Parts

- **Fields to migrate**:
  - `id`: Keep as is
  - `sort`: Keep as is
  - `user_created`: Keep as is
  - `date_created`: Keep as is
  - `date_updated`: Keep as is
  - `title`: Keep as is
  - `order`: Keep as is
  - `content`: Keep as is
  - `quiz`: Keep as is (reference to quiz.id)
  - `time`: Keep as is
  - `passage`: Keep as is (default 0)
  - `simplified_content`: Keep as is
  - `question_count`: Keep as is (default 0)
  - `listen_from`: Keep as is
  - `listen_to`: Keep as is
  - `instruction`: Keep as is
  - `task_instruction`: Keep as is
  - `transcription`: Keep as is
- **Fields to set specific values**:
  - `file_id`: Take from `quiz.listening`
- **Fields to skip**:
  - `questions`: Not needed because `question_sets` will be used

### 1.3. Question Sets

- **Fields to migrate**:
  - `id`: Auto generate
  - `user_created`: Take from the first question in the group
  - `date_created`: Take from the first question in the group
  - `user_updated`: Take from the first question in the group
  - `date_updated`: Take from the first question in the group
  - `sort`: Set based on the order of question sets in the part
- **Fields to set based on grouping rules**:
  - `part_id`: Take from `part.id`
  - `question_type`: Determine based on question type (GAP_FILLING, SINGLE_SELECTION, MATCHING, etc.)
  - `question_count`: Number of questions in question_set
  - `title`: Format "Questions {from}-{to}" (Example: "Questions 1-7", "Questions 8-13")
  - `description`: Take from the instruction of the question type (required field)
  - `content`: Content varies by question type (text with gaps, passages, etc.)
  - `option_title`: Title for options section
  - `options`: Options data in JSON format (varies by question type)
  - `allow_reuse`: Boolean indicating if options can be reused
  - `max_selections`: Maximum number of selections allowed

### 1.4. Questions

- **Fields to migrate**:
  - `id`: Auto generate
  - `status`: Keep as is (default 'draft')
  - `sort`: Keep as is
  - `user_created`: Keep as is
  - `date_created`: Keep as is
  - `user_updated`: Keep as is
  - `date_updated`: Keep as is
  - `title`: Keep as is
  - `content`: Keep as is
  - `locate`: Keep as is
  - `order`: Keep as is
  - `explain`: Keep as is (for explanation field)
  - `description`: Keep as is
  - `content_writing`: Keep as is
  - `time_to_think`: Keep as is
  - `listen_from`: Keep as is
  - `instruction`: Keep as is
  - `writing_graph_image`: Keep as is
  - `writing_graph_description`: Keep as is
  - `writing_graph_type`: Keep as is
  - `audio_url`: Keep as is
  - `time_limit`: Keep as is (default 30)
  - `max_words`: Keep as is
  - `min_words`: Keep as is
  - `text`: Keep as is (for question text)
  - `locate_info`: Keep as is
- **Fields to set specific values**:
  - `quiz_id`: Set = 0 (no longer linked directly to quiz)
  - `part_id`: Set = null (no longer linked directly to part)
  - `type`: Set = "" (legacy field, not used)
  - `gap_fill_in_blank`: Set = null (content moved to question_set)
  - `single_choice_radio`: Set = null (converted to options field)
  - `selection`: Set = null (converted to options field)
  - `mutilple_choice`: Set = null (converted to options field)
  - `selection_option`: Set = null (converted to options field)
  - `question_set_id`: Set to the corresponding question_set.id
- **Fields to set based on question type**:
  - `question_type`: Keep as is (determines the question behavior)
  - `correct_answer`: Used for single answer, question_set.question_types:
    - SINGLE_SELECTION
    - MATCHING
    - NOTE_COMPLETION
    - SINGLE_CHOICE
  - `correct_answers`: Used for multiple answer, question_set.question_types types:
    - GAP_FILLING
    - MULTIPLE_CHOICE_MANY
  - `options`: Used for questions with individual options (SINGLE_CHOICE)

### Example for Quiz

- **Old structure**:

  ```json
  {
    "id": 1714,
    "type": 1,
    "mode": 0,
    "title": "IELTS Reading Test",
    "status": "published",
    "sort": null,
    "time": 60,
    "is_test": null,
    "simplified_id": null,
    "limit_submit": null,
    "thumbnail": null,
    "quiz_code": "",
    "description": null,
    "content": null,
    "parts": [],
    "tags": null,
    "user_created": "user_created",
    "user_updated": "user_updated",
    "date_created": "date_created",
    "date_updated": "date_updated",
    "quiz_part": null,
    "quiz_type": 4,
    "mock_test_id": 46,
    "mock_test_type": 1,
    "listening": null,
    "instruction": null,
    "question": null,
    "samples": null,
    "vote_count": 77,
    "total_submitted": 14508,
    "writing_task_type": null,
    "extra": {
      "user_attempt_count": null
    },
    "speaking_part_type": null,
    "speaking_topic_id": null,
    "speaking_topic": null
  }
  ```

- **New structure**:

  ```json
  {
    "id": 1714,
    "type": 1,
    "mode": 0,
    "title": "Orange 19 Reading - Test 2",
    "status": "published",
    "sort": null,
    "time": 60,
    "is_test": null,
    "simplified_id": null,
    "limit_submit": null,
    "thumbnail": null,
    "quiz_code": "",
    "description": null,
    "content": null,
    "tags": null,
    "user_created": "c3bfa61e-a757-40f2-8711-78a8c9979f79",
    "user_updated": "20e3add8-f7bd-488d-b669-d42f50e7f8e9",
    "date_created": "2024-07-14T07:25:51.829+07:00",
    "date_updated": "2025-06-09T16:38:06.591517+07:00",
    "quiz_part": null,
    "quiz_type": 4,
    "mock_test_id": 46,
    "mock_test_type": 1,
    "listening": null,
    "instruction": null,
    "question": null,
    "samples": null,
    "vote_count": 0,
    "total_submitted": 0,
    "writing_task_type": null,
    "extra": {
      "user_attempt_count": null
    },
    "speaking_part_type": null,
    "speaking_topic_id": null,
    "speaking_topic": null,
    "parts": []
  }
  ```
