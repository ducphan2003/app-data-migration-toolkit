# Kế hoạch Migrate Data IELTS

## Tổng quan
Đây là các nhiệm vụ cần thực hiện để migrate data bài thi IELTS từ cấu trúc cũ sang cấu trúc mới trong hệ thống.

## Quy trình thực hiện

### 1. Nhập Quiz ID trên UI Frontend
- **Giao diện nhập**:
  - Có giao diện frontend để nhập Quiz ID cần migrate
- **Quy trình xử lý**:
  - Backend lưu vào database (bảng import_proccess) và trả về id
  - FE liên tục get thông tin theo id để kiểm tra quá trình migrate
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
Chuyển data từ JSON cũ về cấu trúc AI có thể dễ dàng đọc được:
- Xác định vị trí các câu hỏi, câu trả lời từ cấu trúc JSON cũ
- Xác định content (bài đọc) từ cấu trúc JSON cũ
- Xác định instruction từ cấu trúc JSON cũ
- Xác định vị trí hình ảnh, lấy image_id từ data cũ
- Xác định các thông tin khác (sẽ define chi tiết sau)

### 4. Mapping Structure
Chuyển data từ bước 3 về dạng JSON:
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
2. **Validate bằng logic API**: Bước 5
3. **Validate bằng con người**: Bước 1 (teacher kiểm tra và tinh chỉnh)
4. **Validate cuối cùng**: Bước 2 (trước khi tạo quiz) 


## Steps to implement
1. **Xây dựng giao diện Frontend trước tiên**:
   - Tạo form nhập Quiz ID cần migrate
   - Tạo giao diện hiển thị trạng thái quá trình migrate
   - Tạo giao diện preview data sau khi migrate để teacher có thể kiểm tra
   - Tạo các nút bấm để teacher có thể:
     - Chỉnh sửa data cơ bản
     - Approve để tạo quiz mới
     - Reject hoặc retry nếu có vấn đề

2. **Thiết lập cơ sở dữ liệu**:
   - Tạo bảng `import_proccess` để lưu trữ:
     - ID của quá trình import
     - Status của quá trình
     - Result data
     - Các thông tin log và error messages

3. **Xây dựng các API Backend cơ bản**:
   - API nhận Quiz ID và tạo process import mới
   - API để frontend check status của quá trình migrate
   - API validate data
   - API create quiz mới

4. **Thiết kế các hàm xử lý riêng biệt**:
   - Hàm prepare data (bước 3 trong plan)
   - Hàm mapping structure (bước 4)
   - Hàm validate data (bước 5)
   - Đảm bảo các hàm này được tách biệt để dễ debug và cải thiện

5. **Thiết lập hệ thống logging**:
   - Cấu hình logging cho mỗi bước xử lý
   - Lưu các kết quả trung gian vào database