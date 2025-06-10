# Kế hoạch Import Data IELTS

## Tổng quan
Đây là các nhiệm vụ cần thực hiện để import data bài thi IELTS vào hệ thống.

## Quy trình thực hiện

### 0. Tạo file import (Thủ công)
- **Phạm vi import**: 
  - Teacher sẽ lấy nội dung một bài đọc/nghe (tương ứng với một part)
  - Một bài đó sẽ có một hoặc nhiều question_set
- **Yêu cầu nội dung**:
  - Nội dung được copy một cách đơn giản nhất vào file docs (để giảm workload cho teacher)
  - Cần giữ được cấu trúc/vị trí của checkbox, selection, gap, vị trí image
- **Xác định question type**:
  - Giáo viên nên xác định question_set.type
  - Việc này giúp giảm tải cho AI trong khi việc xác định type khá dễ dàng với giáo viên

### 1. Upload file trên UI Frontend
- **Giao diện upload**:
  - Có giao diện frontend để upload file để xử lý
- **Quy trình xử lý**:
  - Backend lưu vào database (bảng import_proccess) và trả về id
  - FE liên tục get thông tin theo id để kiểm tra quá trình import
- **Kiểm tra kết quả**:
  - Khi status thành công và import_proccess.result có data
  - FE mapping data với giao diện để teacher preview và kiểm tra
- **Xử lý kết quả**:
  - Teacher kiểm tra data/cấu trúc, có thể chỉnh sửa (ở mức cơ bản)
  - Nếu ổn: Call API Create Quiz dựa trên result
  - Nếu không: Reject hoặc retry

### 2. API Create Quiz
- **Validate data**:
  - Kiểm tra các type, cấu trúc dữ liệu, thông tin bắt buộc
  - Trả lỗi rõ ràng
- **Tạo data**: Lưu thông tin vào database

## Quy trình xử lý Backend

### 3. Prepare Data
Chuyển data từ file về cấu trúc AI có thể dễ dàng đọc được:
- Xác định vị trí các câu hỏi, câu trả lời
- Xác định content (bài đọc)
- Xác định instruction
- Xác định vị trí hình ảnh, call API upload file để có image_id
- Xác định các thông tin khác (sẽ define chi tiết sau)

### 4. Mapping Structure
Chuyển data từ bước 4 về dạng JSON:
- Với mỗi question_set.type sẽ cần những thông tin khác nhau
- AI phải xử lý để map data theo cấu trúc model định sẵn

### 5. Validate Data
- Kiểm tra data result (output của AI) trước khi lưu vào import_proccess.result
- API Create Quiz và API validate data sử dụng chung func validate
- Xử lý kết quả:
  - Success: Lưu result, cập nhật trạng thái
  - Fail: Dựa vào error_message để retry (có gợi ý lỗi)

## Lưu ý quan trọng

### Tách biệt chức năng
- Các bước 3, 4, 5 nên được tách thành các func riêng biệt
- Có cơ chế ghi log
- Lưu kết quả cuối cùng của mỗi bước vào import_proccess
- Mục đích: Dễ dàng debug và improve

### Validate nhiều lớp
1. **Validate output**: 
   - Kiểm tra output của các bước 3, 4, 5
   - Sử dụng AI check dựa trên mẫu hoặc quality check
   - Có thể retry (config true/false cho từng bước)
2. **Validate bằng logic API**: Bước 4
3. **Validate bằng con người**: Bước 1 (teacher kiểm tra và tinh chỉnh)
4. **Validate cuối cùng**: Bước 2 (trước khi tạo quiz)
