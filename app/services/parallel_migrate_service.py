import logging
import asyncio
import threading
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from app.repositories.migrate_repository import MigrateRepository
from app.schemas.migrate_schema import PartMigrateRequest, PartMigrateResponse, QuizMergeRequest, QuizMergeResponse
from app.services.migration_workflow import MigrationWorkflow
from app.utils.exceptions import NotFoundException, ValidationError
from app.utils.redis_client import get_redis_client

logger = logging.getLogger(__name__)

class ParallelMigrateService:
    """Service xử lý migrate các part song song"""
    
    def __init__(self, migrate_repo: MigrateRepository):
        self.migrate_repo = migrate_repo
        self.migration_workflow = MigrationWorkflow(migrate_repo)
        self.redis_client = get_redis_client()
    
    def split_quiz_into_parts(self, quiz_data: Dict[str, Any], user_id: str) -> List[PartMigrateRequest]:
        """
        Tách quiz thành các part riêng biệt để xử lý song song
        """
        try:
            quiz_id = str(quiz_data.get("id"))
            quiz_title = quiz_data.get("title", "")
            quiz_type = self._determine_quiz_type(quiz_data)
            parts = quiz_data.get("parts", [])
            
            if len(parts) != 3:
                raise ValidationError(f"Quiz phải có đúng 3 parts, hiện tại có {len(parts)} parts")
            
            part_requests = []
            
            for i, part in enumerate(parts, 1):
                part_request = PartMigrateRequest(
                    quiz_id=quiz_id,
                    quiz_title=quiz_title,
                    quiz_type=quiz_type,
                    quiz_time=quiz_data.get("time"),
                    quiz_description=quiz_data.get("description"),
                    listening_file_id=quiz_data.get("listening") if quiz_type == "listening" else None,
                    part_index=i,
                    part_title=part.get("title", f"Part {i}"),
                    part_content=part.get("content"),
                    part_description=part.get("description"),
                    part_time=part.get("time"),
                    questions=part.get("questions", []),
                    total_parts=len(parts),
                    user_id=user_id
                )
                part_requests.append(part_request)
            
            logger.info(f"Split quiz {quiz_id} into {len(part_requests)} part requests")
            return part_requests
            
        except Exception as e:
            logger.error(f"Error splitting quiz into parts: {str(e)}")
            raise e
    
    def process_parts_parallel(self, part_requests: List[PartMigrateRequest]) -> Dict[str, str]:
        """
        Xử lý các parts song song và trả về part_migrate_ids
        """
        try:
            part_migrate_ids = {}
            threads = []
            
            # Tạo thread cho mỗi part
            for part_request in part_requests:
                part_migrate_id = str(uuid.uuid4())
                part_migrate_ids[f"part_{part_request.part_index}"] = part_migrate_id
                
                # Lưu part request vào Redis với TTL
                self._store_part_request(part_migrate_id, part_request)
                
                # Tạo thread xử lý part
                thread = threading.Thread(
                    target=self._process_single_part,
                    args=(part_migrate_id, part_request)
                )
                thread.daemon = True
                threads.append(thread)
                thread.start()
                
                logger.info(f"Started processing part {part_request.part_index} with ID {part_migrate_id}")
            
            # Không đợi threads hoàn thành, chỉ trả về IDs để client poll
            logger.info(f"Started {len(threads)} parallel part processing threads")
            
            return part_migrate_ids
            
        except Exception as e:
            logger.error(f"Error starting parallel part processing: {str(e)}")
            raise e
    
    def get_part_migrate_status(self, part_migrate_id: str) -> PartMigrateResponse:
        """
        Lấy trạng thái migrate của một part
        """
        try:
            # Lấy từ Redis
            part_status = self._get_part_status(part_migrate_id)
            
            if not part_status:
                raise NotFoundException(f"Không tìm thấy part migration với ID {part_migrate_id}")
            
            return PartMigrateResponse(**part_status)
            
        except Exception as e:
            logger.error(f"Error getting part migrate status: {str(e)}")
            raise e
    
    def merge_parts_to_quiz(self, merge_request: QuizMergeRequest) -> str:
        """
        Merge các parts đã migrate thành quiz hoàn chỉnh
        """
        try:
            quiz_merge_id = str(uuid.uuid4())
            
            # Lưu merge request
            self._store_merge_request(quiz_merge_id, merge_request)
            
            # Chạy merge trong background thread
            thread = threading.Thread(
                target=self._merge_parts_background,
                args=(quiz_merge_id, merge_request)
            )
            thread.daemon = True
            thread.start()
            
            logger.info(f"Started merging parts for quiz {merge_request.quiz_id} with merge ID {quiz_merge_id}")
            
            return quiz_merge_id
            
        except Exception as e:
            logger.error(f"Error starting parts merge: {str(e)}")
            raise e
    
    def get_quiz_merge_status(self, quiz_merge_id: str) -> QuizMergeResponse:
        """
        Lấy trạng thái merge quiz
        """
        try:
            merge_status = self._get_merge_status(quiz_merge_id)
            
            if not merge_status:
                raise NotFoundException(f"Không tìm thấy quiz merge với ID {quiz_merge_id}")
            
            return QuizMergeResponse(**merge_status)
            
        except Exception as e:
            logger.error(f"Error getting quiz merge status: {str(e)}")
            raise e
    
    def _process_single_part(self, part_migrate_id: str, part_request: PartMigrateRequest):
        """
        Xử lý migrate một part riêng lẻ trong background thread
        """
        try:
            logger.info(f"Starting migration for part {part_request.part_index}")
            
            # Cập nhật trạng thái bắt đầu
            self._update_part_status(part_migrate_id, {
                "part_migrate_id": part_migrate_id,
                "quiz_id": part_request.quiz_id,
                "part_index": part_request.part_index,
                "status": "processing",
                "progress_percentage": 0.0,
                "created_at": datetime.utcnow().isoformat(),
                "error_message": None
            })
            
            # Chuyển part request thành format cho migration workflow
            input_data = {
                "id": part_request.quiz_id,
                "title": part_request.quiz_title,
                "type": 1 if part_request.quiz_type == "reading" else 2,
                "time": part_request.quiz_time,
                "description": part_request.quiz_description,
                "listening": part_request.listening_file_id,
                "parts": [{
                    "title": part_request.part_title,
                    "content": part_request.part_content,
                    "description": part_request.part_description,
                    "time": part_request.part_time,
                    "questions": part_request.questions
                }]
            }
            
            # Chạy migration workflow cho part này
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                final_state = loop.run_until_complete(
                    self.migration_workflow.run_migration(
                        part_migrate_id, part_request.user_id, input_data, part_request.quiz_type
                    )
                )
                
                # Extract kết quả và validate
                actual_state = self.migration_workflow._extract_actual_state(final_state)
                final_result = actual_state.get('final_result', {})
                
                logger.info(f"Raw migration result for part {part_request.part_index}: Parts={len(final_result.get('parts', []))}, QSets={len(final_result.get('question_sets', []))}, Questions={len(final_result.get('questions', []))}")
                
                # Debug detailed structure
                self._debug_migration_structure(part_request.part_index, final_result)
                
                if final_result and 'parts' in final_result and len(final_result['parts']) > 0:
                    # Lấy part đầu tiên (vì chúng ta chỉ gửi 1 part vào migration)
                    migrated_part = final_result['parts'][0]
                    all_question_sets = final_result.get('question_sets', [])
                    all_questions = final_result.get('questions', [])
                    
                    # Filter question_sets và questions thuộc về part này
                    part_id = migrated_part.get('id')
                    if part_id:
                        # Filter question_sets thuộc part này
                        migrated_question_sets = [qs for qs in all_question_sets if qs.get('part_id') == part_id]
                        
                        # Filter questions thuộc các question_sets của part này
                        question_set_ids = [qs.get('id') for qs in migrated_question_sets]
                        migrated_questions = [q for q in all_questions if q.get('question_set_id') in question_set_ids]
                    else:
                        # Fallback: lấy tất cả nếu không có part_id
                        migrated_question_sets = all_question_sets
                        migrated_questions = all_questions
                    
                    # Cập nhật part index để đúng thứ tự
                    migrated_part['sort'] = part_request.part_index
                    migrated_part['order'] = part_request.part_index
                    
                    # Validate kết quả
                    if len(migrated_question_sets) == 0:
                        logger.warning(f"Part {part_request.part_index} has no question_sets after filtering")
                    
                    if len(migrated_questions) == 0:
                        logger.warning(f"Part {part_request.part_index} has no questions after filtering")
                    
                    logger.info(f"Part {part_request.part_index} processed: {len(migrated_question_sets)} question_sets, {len(migrated_questions)} questions")
                    
                    # Cập nhật trạng thái hoàn thành
                    self._update_part_status(part_migrate_id, {
                        "status": "completed",
                        "progress_percentage": 100.0,
                        "migrated_part": migrated_part,
                        "migrated_question_sets": migrated_question_sets,
                        "migrated_questions": migrated_questions,
                        "completed_at": datetime.utcnow().isoformat()
                    })
                    
                    logger.info(f"✅ Successfully migrated part {part_request.part_index}")
                else:
                    raise Exception(f"Migration workflow did not return expected results for part {part_request.part_index}. Parts found: {len(final_result.get('parts', []))}")
                    
            finally:
                loop.close()
            
        except Exception as e:
            error_msg = f"Error migrating part {part_request.part_index}: {str(e)}"
            logger.error(error_msg)
            
            # Cập nhật trạng thái lỗi
            self._update_part_status(part_migrate_id, {
                "status": "failed",
                "error_message": error_msg,
                "completed_at": datetime.utcnow().isoformat()
            })
    
    def _merge_parts_background(self, quiz_merge_id: str, merge_request: QuizMergeRequest):
        """
        Merge các parts trong background thread với logic filter parts rỗng
        """
        try:
            logger.info(f"Starting merge for quiz {merge_request.quiz_id}")
            
            # Cập nhật trạng thái bắt đầu
            self._update_merge_status(quiz_merge_id, {
                "quiz_merge_id": quiz_merge_id,
                "quiz_id": merge_request.quiz_id,
                "status": "processing",
                "created_at": datetime.utcnow().isoformat(),
                "error_message": None
            })
            
            # Collect data từ các parts đã migrate
            parts_collection = []
            
            for i, part_migrate_id in enumerate(merge_request.part_migrate_ids, 1):
                part_status = self._get_part_status(part_migrate_id)
                
                if not part_status or part_status.get("status") != "completed":
                    raise Exception(f"Part migration {part_migrate_id} chưa hoàn thành")
                
                parts_collection.append({
                    'part_index': i,
                    'part': part_status.get("migrated_part"),
                    'question_sets': part_status.get("migrated_question_sets", []),
                    'questions': part_status.get("migrated_questions", [])
                })
                
                logger.info(f"Collected part {i}: {len(part_status.get('migrated_question_sets', []))} question sets, {len(part_status.get('migrated_questions', []))} questions")
            
            # Filter và organize data đúng cách - chỉ giữ parts có question_sets không rỗng
            final_parts = []
            final_question_sets = []
            final_questions = []
            quiz_info = None
            
            for part_data in parts_collection:
                part = part_data['part']
                question_sets = part_data['question_sets']
                questions = part_data['questions']
                part_index = part_data['part_index']
                
                # Kiểm tra part có hợp lệ không (có question_sets và questions)
                if part and question_sets and len(question_sets) > 0 and questions and len(questions) > 0:
                    # Đảm bảo part có sort/order đúng
                    if 'sort' not in part or part['sort'] is None:
                        part['sort'] = part_index
                    if 'order' not in part or part['order'] is None:
                        part['order'] = part_index
                    
                    # Lưu quiz info từ part đầu tiên hợp lệ
                    if quiz_info is None:
                        quiz_info = {
                            "id": merge_request.quiz_id,
                            "title": part.get("title", f"Quiz {merge_request.quiz_id}"),
                            "status": "published",
                            "is_public": True,
                            "is_test": True
                        }
                    
                    final_parts.append(part)
                    final_question_sets.extend(question_sets)
                    final_questions.extend(questions)
                    
                    logger.info(f"✓ Added valid part {part_index} (sort: {part.get('sort')}) with {len(question_sets)} question sets and {len(questions)} questions")
                else:
                    logger.warning(f"✗ Skipped part {part_index} - empty question_sets or questions. Part: {part is not None}, QSets: {len(question_sets) if question_sets else 0}, Questions: {len(questions) if questions else 0}")
            
            # Sắp xếp parts theo thứ tự
            final_parts.sort(key=lambda x: x.get('sort', 0))
            
            # Validate kết quả
            if len(final_parts) == 0:
                raise Exception("Không có part nào hợp lệ sau khi filter (tất cả parts đều rỗng question_sets)")
            
            # Kiểm tra nếu có quá nhiều parts (có thể do duplicate)
            if len(final_parts) > 3:
                logger.warning(f"Found {len(final_parts)} parts, expected maximum 3. Keeping only first 3 by sort order.")
                final_parts = final_parts[:3]
                
                # Filter question_sets và questions tương ứng với 3 parts được giữ lại
                valid_part_ids = [p.get('id') for p in final_parts if p.get('id')]
                if valid_part_ids:
                    original_qs_count = len(final_question_sets)
                    original_q_count = len(final_questions)
                    
                    final_question_sets = [qs for qs in final_question_sets if qs.get('part_id') in valid_part_ids]
                    final_questions = [q for q in final_questions if any(qs.get('id') == q.get('question_set_id') for qs in final_question_sets)]
                    
                    logger.info(f"Filtered question_sets: {original_qs_count} -> {len(final_question_sets)}")
                    logger.info(f"Filtered questions: {original_q_count} -> {len(final_questions)}")
            
            # Re-index parts để đảm bảo thứ tự 1, 2, 3
            for i, part in enumerate(final_parts, 1):
                part['sort'] = i
                part['order'] = i
            
            # Tạo quiz hoàn chỉnh với data đã cleaned
            final_quiz = {
                "quiz": quiz_info or {
                    "id": merge_request.quiz_id,
                    "title": f"Merged Quiz {merge_request.quiz_id}",
                    "status": "published",
                    "is_public": True,
                    "is_test": True
                },
                "parts": final_parts,
                "question_sets": final_question_sets,
                "questions": final_questions
            }
            
            # Log kết quả cuối chi tiết
            logger.info("="*50)
            logger.info(f"🎯 MERGE RESULT for Quiz {merge_request.quiz_id}:")
            logger.info(f"   📚 Final Parts: {len(final_parts)}")
            for i, part in enumerate(final_parts, 1):
                logger.info(f"      Part {i}: {part.get('title', 'No title')} (sort: {part.get('sort')})")
            logger.info(f"   📝 Final Question Sets: {len(final_question_sets)}")
            logger.info(f"   ❓ Final Questions: {len(final_questions)}")
            logger.info("="*50)
            
            # Cập nhật trạng thái hoàn thành
            self._update_merge_status(quiz_merge_id, {
                "status": "completed",
                "final_quiz": self._validate_final_quiz_structure(final_quiz),
                "total_parts": len(final_parts),
                "total_question_sets": len(final_question_sets),
                "total_questions": len(final_questions),
                "completed_at": datetime.utcnow().isoformat()
            })
            
            logger.info(f"✅ Successfully merged quiz {merge_request.quiz_id}")
            
        except Exception as e:
            error_msg = f"❌ Error merging quiz {merge_request.quiz_id}: {str(e)}"
            logger.error(error_msg)
            logger.exception("Full merge error details:")
            
            # Cập nhật trạng thái lỗi
            self._update_merge_status(quiz_merge_id, {
                "status": "failed",
                "error_message": error_msg,
                "completed_at": datetime.utcnow().isoformat()
            })
    
    def _determine_quiz_type(self, input_data: Dict[str, Any]) -> str:
        """Xác định loại quiz"""
        quiz_type = input_data.get("type")
        
        if quiz_type == 1:
            return "reading"
        elif quiz_type == 2:
            return "listening"
        else:
            return "reading" if not input_data.get("listening") else "listening"
    
    def _store_part_request(self, part_migrate_id: str, part_request: PartMigrateRequest):
        """Lưu part request vào Redis"""
        key = f"part_request:{part_migrate_id}"
        self.redis_client.setex(key, 3600, json.dumps(part_request.dict()))  # TTL 1 hour
    
    def _store_merge_request(self, quiz_merge_id: str, merge_request: QuizMergeRequest):
        """Lưu merge request vào Redis"""
        key = f"merge_request:{quiz_merge_id}"
        self.redis_client.setex(key, 3600, json.dumps(merge_request.dict()))  # TTL 1 hour
    
    def _update_part_status(self, part_migrate_id: str, status_data: Dict[str, Any]):
        """Cập nhật trạng thái part vào Redis"""
        key = f"part_status:{part_migrate_id}"
        
        # Lấy status hiện tại để merge
        current_status = self._get_part_status(part_migrate_id) or {}
        current_status.update(status_data)
        
        self.redis_client.setex(key, 3600, json.dumps(current_status, default=str))  # TTL 1 hour
    
    def _update_merge_status(self, quiz_merge_id: str, status_data: Dict[str, Any]):
        """Cập nhật trạng thái merge vào Redis"""
        key = f"merge_status:{quiz_merge_id}"
        
        # Lấy status hiện tại để merge
        current_status = self._get_merge_status(quiz_merge_id) or {}
        current_status.update(status_data)
        
        self.redis_client.setex(key, 3600, json.dumps(current_status, default=str))  # TTL 1 hour
    
    def _get_part_status(self, part_migrate_id: str) -> Optional[Dict[str, Any]]:
        """Lấy trạng thái part từ Redis"""
        key = f"part_status:{part_migrate_id}"
        status_json = self.redis_client.get(key)
        
        if status_json:
            return json.loads(status_json)
        return None
    
    def _get_merge_status(self, quiz_merge_id: str) -> Optional[Dict[str, Any]]:
        """Lấy trạng thái merge từ Redis"""
        key = f"merge_status:{quiz_merge_id}"
        status_json = self.redis_client.get(key)
        
        if status_json:
            return json.loads(status_json)
        return None
    
    def _debug_migration_structure(self, part_index: int, final_result: Dict[str, Any]):
        """
        Debug helper để log structure của migration result
        """
        logger.debug(f"🔍 DEBUG Part {part_index} Migration Structure:")
        
        parts = final_result.get('parts', [])
        logger.debug(f"   Parts ({len(parts)}):")
        for i, part in enumerate(parts):
            logger.debug(f"      Part {i+1}: ID={part.get('id')}, Title='{part.get('title', 'No title')}', Sort={part.get('sort')}")
        
        question_sets = final_result.get('question_sets', [])
        logger.debug(f"   Question Sets ({len(question_sets)}):")
        for i, qs in enumerate(question_sets[:5]):  # Chỉ log 5 đầu để tránh spam
            logger.debug(f"      QSet {i+1}: ID={qs.get('id')}, PartID={qs.get('part_id')}, Title='{qs.get('title', 'No title')[:30]}...'")
        if len(question_sets) > 5:
            logger.debug(f"      ... và {len(question_sets) - 5} question sets khác")
        
        questions = final_result.get('questions', [])
        logger.debug(f"   Questions ({len(questions)}):")
        for i, q in enumerate(questions[:5]):  # Chỉ log 5 đầu
            logger.debug(f"      Q {i+1}: ID={q.get('id')}, QSetID={q.get('question_set_id')}, Title='{q.get('title', 'No title')[:30]}...'")
        if len(questions) > 5:
            logger.debug(f"      ... và {len(questions) - 5} questions khác")
    
    def _validate_final_quiz_structure(self, final_quiz: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate và cleanup final quiz structure
        """
        logger.info("🔍 Validating final quiz structure...")
        
        # Validate basic structure
        if 'quiz' not in final_quiz:
            raise Exception("Missing 'quiz' section in final result")
        if 'parts' not in final_quiz:
            raise Exception("Missing 'parts' section in final result")
        if 'question_sets' not in final_quiz:
            raise Exception("Missing 'question_sets' section in final result")
        if 'questions' not in final_quiz:
            raise Exception("Missing 'questions' section in final result")
        
        # Validate parts
        parts = final_quiz['parts']
        if len(parts) == 0:
            raise Exception("No valid parts found in final quiz")
        
        if len(parts) > 3:
            logger.warning(f"Found {len(parts)} parts, maximum should be 3. Keeping first 3.")
            parts = parts[:3]
            final_quiz['parts'] = parts
        
        # Ensure parts are properly indexed
        for i, part in enumerate(parts, 1):
            if not part.get('id'):
                logger.warning(f"Part {i} missing ID, generating one")
                part['id'] = f"part_{i}_{int(datetime.utcnow().timestamp())}"
            part['sort'] = i
            part['order'] = i
        
        # Clean question_sets - chỉ giữ những sets thuộc các parts hợp lệ
        valid_part_ids = [p['id'] for p in parts]
        original_qsets = final_quiz['question_sets']
        valid_qsets = [qs for qs in original_qsets if qs.get('part_id') in valid_part_ids]
        
        if len(valid_qsets) != len(original_qsets):
            logger.info(f"Filtered question_sets: {len(original_qsets)} -> {len(valid_qsets)}")
        
        # Clean questions - chỉ giữ những questions thuộc valid question_sets
        valid_qset_ids = [qs['id'] for qs in valid_qsets if qs.get('id')]
        original_questions = final_quiz['questions']
        valid_questions = [q for q in original_questions if q.get('question_set_id') in valid_qset_ids]
        
        if len(valid_questions) != len(original_questions):
            logger.info(f"Filtered questions: {len(original_questions)} -> {len(valid_questions)}")
        
        # Update final quiz
        final_quiz['question_sets'] = valid_qsets
        final_quiz['questions'] = valid_questions
        
        # Final validation
        if len(valid_qsets) == 0:
            raise Exception("No valid question_sets remain after cleanup")
        
        if len(valid_questions) == 0:
            raise Exception("No valid questions remain after cleanup")
        
        logger.info(f"✅ Final quiz validation passed: {len(parts)} parts, {len(valid_qsets)} question_sets, {len(valid_questions)} questions")
        
        return final_quiz 