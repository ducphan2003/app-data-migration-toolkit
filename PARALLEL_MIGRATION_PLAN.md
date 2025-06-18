# Kế hoạch Migration Song song cho Quiz với 3 Parts

## Tổng quan

Hiện tại hệ thống xử lý migration quiz có vấn đề khi quiz có 3 parts:
- Request body trở nên rất dài
- Xử lý tuần tự gây chậm
- Khó quản lý tiến độ từng part

**Giải pháp**: Tách 3 parts thành các request riêng biệt, xử lý song song qua AI, sau đó merge lại thành 1 response cuối cùng.

## Kiến trúc mới

### 1. Flow chính

```
Client Request (Quiz với 3 parts) 
    ↓
Split thành 3 Part Requests
    ↓
Process 3 Parts song song qua AI
    ↓
Poll status từng Part
    ↓
Merge 3 Parts thành Quiz hoàn chỉnh
    ↓
Response final quiz
```

### 2. Components đã tạo

#### 2.1 Schemas mới (`app/schemas/migrate_schema.py`)

- `PartMigrateRequest`: Request cho từng part riêng lẻ
- `PartMigrateResponse`: Response status của part migration
- `QuizMergeRequest`: Request merge các parts thành quiz
- `QuizMergeResponse`: Response status của quiz merge

#### 2.2 Service mới (`app/services/parallel_migrate_service.py`)

- `ParallelMigrateService`: Service chính xử lý parallel migration
- Methods:
  - `split_quiz_into_parts()`: Tách quiz thành 3 part requests
  - `process_parts_parallel()`: Xử lý 3 parts song song
  - `merge_parts_to_quiz()`: Merge các parts đã migrate
  - `get_part_migrate_status()`: Lấy status từng part
  - `get_quiz_merge_status()`: Lấy status merge quiz

#### 2.3 Controller mới (`app/controllers/parallel_migrate_api.py`)

- API endpoints cho parallel migration
- Endpoints:
  - `POST /migrate-quiz-parallel`: Bắt đầu migrate quiz song song
  - `GET /migrate-part-status/<id>`: Lấy status part
  - `POST /check-all-parts-status`: Kiểm tra status tất cả parts
  - `POST /merge-quiz-parts`: Merge parts thành quiz
  - `GET /merge-quiz-status/<id>`: Lấy status merge

## API Usage Flow

### Bước 1: Bắt đầu Migration Song song

```http
POST /api/migrate-quiz-parallel
Content-Type: application/json
Authorization: Bearer <token>

{
  "id": "123",
  "title": "IELTS Reading Test",
  "type": 1,
  "time": 60,
  "parts": [
    {
      "title": "Part 1",
      "content": "Reading passage 1...",
      "questions": [...]
    },
    {
      "title": "Part 2", 
      "content": "Reading passage 2...",
      "questions": [...]
    },
    {
      "title": "Part 3",
      "content": "Reading passage 3...",
      "questions": [...]
    }
  ]
}
```

**Response:**
```json
{
  "message": "Quiz đã được tách thành 3 parts và đang xử lý song song",
  "data": {
    "quiz_id": "123",
    "total_parts": 3,
    "part_migrate_ids": {
      "part_1": "uuid-part-1",
      "part_2": "uuid-part-2", 
      "part_3": "uuid-part-3"
    },
    "instructions": {
      "next_step": "Poll các part_migrate_ids để theo dõi tiến độ"
    }
  }
}
```

### Bước 2: Poll Status các Parts

```http
GET /api/migrate-part-status/uuid-part-1
Authorization: Bearer <token>
```

**Response:**
```json
{
  "data": {
    "part_migrate_id": "uuid-part-1",
    "quiz_id": "123",
    "part_index": 1,
    "status": "completed", // processing, completed, failed
    "progress_percentage": 100.0,
    "migrated_part": {...}, // Part data đã migrate
    "migrated_question_sets": [...],
    "migrated_questions": [...],
    "created_at": "2024-01-01T10:00:00Z",
    "completed_at": "2024-01-01T10:05:00Z"
  }
}
```

### Bước 3: Kiểm tra tất cả Parts hoàn thành

```http
POST /api/check-all-parts-status
Content-Type: application/json
Authorization: Bearer <token>

{
  "part_migrate_ids": {
    "part_1": "uuid-part-1",
    "part_2": "uuid-part-2",
    "part_3": "uuid-part-3"
  }
}
```

**Response:**
```json
{
  "data": {
    "parts_status": {
      "part_1": {"status": "completed", ...},
      "part_2": {"status": "completed", ...},
      "part_3": {"status": "completed", ...}
    },
    "summary": {
      "all_completed": true,
      "any_failed": false,
      "ready_for_merge": true
    }
  }
}
```

### Bước 4: Merge Parts thành Quiz hoàn chỉnh

```http
POST /api/merge-quiz-parts
Content-Type: application/json
Authorization: Bearer <token>

{
  "quiz_id": "123",
  "part_migrate_ids": {
    "part_1": "uuid-part-1",
    "part_2": "uuid-part-2",
    "part_3": "uuid-part-3"
  }
}
```

**Response:**
```json
{
  "message": "Bắt đầu merge các parts thành quiz hoàn chỉnh",
  "data": {
    "quiz_merge_id": "uuid-merge-123",
    "quiz_id": "123",
    "status": "processing",
    "instructions": {
      "next_step": "Poll quiz_merge_id để theo dõi tiến độ merge"
    }
  }
}
```

### Bước 5: Lấy kết quả final

```http
GET /api/merge-quiz-status/uuid-merge-123
Authorization: Bearer <token>
```

**Response:**
```json
{
  "data": {
    "quiz_merge_id": "uuid-merge-123",
    "quiz_id": "123", 
    "status": "completed",
    "final_quiz": {
      "quiz": {...},
      "parts": [...],
      "question_sets": [...],
      "questions": [...]
    },
    "total_parts": 3,
    "total_question_sets": 15,
    "total_questions": 40,
    "created_at": "2024-01-01T10:10:00Z",
    "completed_at": "2024-01-01T10:12:00Z"
  }
}
```

## Lợi ích

### 1. Hiệu suất
- **Tăng tốc 3x**: 3 parts xử lý song song thay vì tuần tự
- **Giảm request size**: Mỗi request chỉ chứa 1 part thay vì 3 parts
- **Tối ưu resource**: AI agents hoạt động song song

### 2. User Experience  
- **Real-time progress**: Theo dõi tiến độ từng part riêng biệt
- **Better error handling**: Lỗi ở 1 part không ảnh hưởng 2 parts khác
- **Granular control**: Có thể retry từng part riêng lẻ

### 3. Scalability
- **Horizontal scaling**: Dễ dàng mở rộng cho nhiều parts hơn
- **Load balancing**: Phân tải AI processing
- **Resource optimization**: Sử dụng Redis để cache kết quả

## Technical Implementation

### 1. Storage Strategy
- **Redis**: Lưu trữ trạng thái và kết quả tạm thời
- **TTL**: 1 giờ cho tất cả cache keys
- **Key patterns**:
  - `part_request:{part_migrate_id}`
  - `part_status:{part_migrate_id}` 
  - `merge_request:{quiz_merge_id}`
  - `merge_status:{quiz_merge_id}`

### 2. Concurrency Strategy
- **Threading**: Mỗi part chạy trong thread riêng
- **Async/Await**: Migration workflow vẫn sử dụng async
- **Event Loop**: Tạo loop riêng cho mỗi thread

### 3. Error Handling
- **Isolation**: Lỗi ở 1 part không ảnh hưởng parts khác
- **Retry mechanism**: Có thể retry từng part riêng lẻ
- **Graceful degradation**: Merge chỉ proceed khi tất cả parts hoàn thành

## Deployment Steps

### 1. Cập nhật app factory
```python
# app/factory.py
from app.controllers.parallel_migrate_api import create_parallel_migrate_controllers

def create_app():
    # ... existing code ...
    
    # Register new parallel migration blueprint
    parallel_migrate_controllers = create_parallel_migrate_controllers(migrate_repository)
    app.register_blueprint(parallel_migrate_controllers, url_prefix='/api')
    
    return app
```

### 2. Test API endpoints
```bash
# Test split và parallel processing
curl -X POST http://localhost:5000/api/migrate-quiz-parallel \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d @quiz_with_3_parts.json

# Test status checking  
curl -X GET http://localhost:5000/api/migrate-part-status/<part_id> \
  -H "Authorization: Bearer <token>"

# Test merge
curl -X POST http://localhost:5000/api/merge-quiz-parts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"quiz_id": "123", "part_migrate_ids": {...}}'
```

### 3. Frontend integration
```javascript
// Example frontend implementation
class ParallelMigrationClient {
  async migrateQuizParallel(quizData) {
    const response = await fetch('/api/migrate-quiz-parallel', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(quizData)
    });
    
    const result = await response.json();
    return result.data;
  }
  
  async pollPartsStatus(partMigrateIds) {
    const promises = Object.entries(partMigrateIds).map(([partName, partId]) =>
      fetch(`/api/migrate-part-status/${partId}`)
        .then(res => res.json())
        .then(data => [partName, data])
    );
    
    const results = await Promise.all(promises);
    return Object.fromEntries(results);
  }
  
  async mergeQuizParts(quizId, partMigrateIds) {
    const response = await fetch('/api/merge-quiz-parts', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ quiz_id: quizId, part_migrate_ids: partMigrateIds })
    });
    
    return response.json();
  }
}
```

## Monitoring & Observability

### 1. Logging
- Log mỗi bước của parallel processing
- Track timing cho performance optimization
- Error logging với stack trace đầy đủ

### 2. Metrics
- Part processing time
- Success/failure rates 
- Concurrent processing load
- Redis cache hit/miss rates

### 3. Alerting
- Alert khi migration time quá lâu
- Alert khi failure rate cao
- Alert khi Redis storage gần full

## Future Enhancements

### 1. Dynamic Partitioning
- Hỗ trợ quiz với số parts khác nhau (không chỉ 3)
- Auto-split based on content size

### 2. Advanced Queuing
- Implement proper job queue (Celery/RQ)
- Priority-based processing
- Retry with exponential backoff

### 3. Real-time Updates
- WebSocket cho real-time status updates
- Progress streaming cho better UX

### 4. Caching Optimization
- Cache AI analysis results
- Smart cache invalidation
- Distributed caching với Redis Cluster

---

Kế hoạch này sẽ cải thiện đáng kể hiệu suất và trải nghiệm người dùng khi xử lý quiz có nhiều parts. 