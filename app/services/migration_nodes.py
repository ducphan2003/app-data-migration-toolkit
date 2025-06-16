import logging
import json
from typing import Dict, Any, List
from datetime import datetime
import time

from app.schemas.migration_state import MigrationState, MigrationStatus, QualityMetrics

logger = logging.getLogger(__name__)

class MigrationNodes:
    """Các Node xử lý trong LangGraph migration workflow"""
    
    @staticmethod
    def analyze_node(state: MigrationState) -> MigrationState:
        """
        Node 1: Phân tích cấu trúc dữ liệu đầu vào
        """
        logger.info(f"Starting analyze_node for process {state['migrate_process_id']}")
        
        try:
            state["status"] = MigrationStatus.ANALYZING
            state["current_step"] = "analyze"
            state["progress_percentage"] = 10.0
            
            # Log bắt đầu
            state["processing_logs"].append({
                "step": "analyze",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Starting data analysis",
                "level": "info"
            })
            
            input_data = state["raw_input_data"]
            quiz_type = state["quiz_type"]
            
            # Phân tích cấu trúc
            analyzed_data = {
                "quiz_info": {
                    "id": input_data.get("id"),
                    "title": input_data.get("title"),
                    "type": quiz_type,
                    "time_limit": input_data.get("time", 0) * 60,
                    "description": input_data.get("description"),
                    "listening_file_id": input_data.get("listening") if quiz_type == "listening" else None
                },
                "parts_analysis": [],
                "questions_analysis": [],
                "metadata": {
                    "total_parts": len(input_data.get("parts", [])),
                    "total_questions": 0,
                    "question_types_found": set(),
                    "analysis_timestamp": datetime.utcnow().isoformat()
                }
            }
            
            # Phân tích từng part
            total_questions = 0
            question_types = set()
            
            for part_idx, part in enumerate(input_data.get("parts", []), 1):
                part_analysis = {
                    "part_index": part_idx,
                    "title": part.get("title", f"Part {part_idx}"),
                    "description": part.get("description"),
                    "questions_count": len(part.get("questions", [])),
                    "question_types": set()
                }
                
                # Phân tích questions trong part
                for question in part.get("questions", []):
                    total_questions += 1
                    q_type = MigrationNodes._detect_question_type(question)
                    question_types.add(q_type)
                    part_analysis["question_types"].add(q_type)
                    
                    analyzed_data["questions_analysis"].append({
                        "part_index": part_idx,
                        "question_id": question.get("id"),
                        "detected_type": q_type,
                        "original_data": question
                    })
                
                # Convert set to list for JSON serialization
                part_analysis["question_types"] = list(part_analysis["question_types"])
                analyzed_data["parts_analysis"].append(part_analysis)
            
            # Cập nhật metadata
            analyzed_data["metadata"]["total_questions"] = total_questions
            analyzed_data["metadata"]["question_types_found"] = list(question_types)
            
            # Cập nhật state
            state["analyzed_data"] = analyzed_data
            state["total_parts"] = len(input_data.get("parts", []))
            state["progress_percentage"] = 25.0
            
            # Cập nhật quality metrics
            state["quality_metrics"]["total_questions"] = total_questions
            
            # Log thành công
            state["processing_logs"].append({
                "step": "analyze",
                "timestamp": datetime.utcnow().isoformat(),
                "message": f"Analysis completed. Found {total_questions} questions in {len(analyzed_data['parts_analysis'])} parts",
                "level": "info",
                "details": {
                    "total_questions": total_questions,
                    "question_types": list(question_types)
                }
            })
            
            logger.info(f"Analyze node completed for process {state['migrate_process_id']}")
            
        except Exception as e:
            error_msg = f"Error in analyze_node: {str(e)}"
            logger.error(error_msg)
            state["errors"].append(error_msg)
            state["status"] = MigrationStatus.FAILED
            
            state["processing_logs"].append({
                "step": "analyze",
                "timestamp": datetime.utcnow().isoformat(),
                "message": error_msg,
                "level": "error"
            })
        
        return state
    
    @staticmethod
    def mapping_node(state: MigrationState) -> MigrationState:
        """
        Node 2: Áp dụng rules chuyển đổi dữ liệu
        """
        logger.info(f"Starting mapping_node for process {state['migrate_process_id']}")
        
        try:
            state["status"] = MigrationStatus.MAPPING
            state["current_step"] = "mapping"
            state["progress_percentage"] = 50.0
            
            # Log bắt đầu
            state["processing_logs"].append({
                "step": "mapping",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Starting data mapping",
                "level": "info"
            })
            
            analyzed_data = state["analyzed_data"]
            quiz_info = analyzed_data["quiz_info"]
            
            # Tạo cấu trúc mới
            mapped_data = {
                "quiz": {
                    "id": "auto_generate",
                    "title": quiz_info["title"],
                    "description": quiz_info["description"],
                    "status": "published",
                    "type": quiz_info["type"],
                    "time_limit": quiz_info["time_limit"],
                    "vote_count": 0,
                    "total_submitted": 0,
                    "user_created": "system",
                    "date_created": datetime.utcnow().isoformat(),
                    "parts": []
                }
            }
            
            # Thêm listening_file_id nếu có
            if quiz_info.get("listening_file_id"):
                mapped_data["quiz"]["listening_file_id"] = quiz_info["listening_file_id"]
            
            # Mapping từng part
            successfully_mapped = 0
            failed_mappings = 0
            
            for part_analysis in analyzed_data["parts_analysis"]:
                try:
                    mapped_part = MigrationNodes._map_part(part_analysis, state["raw_input_data"]["parts"][part_analysis["part_index"] - 1])
                    mapped_data["quiz"]["parts"].append(mapped_part)
                    successfully_mapped += 1
                    
                    state["processing_logs"].append({
                        "step": "mapping",
                        "timestamp": datetime.utcnow().isoformat(),
                        "message": f"Successfully mapped part {part_analysis['part_index']}",
                        "level": "info"
                    })
                    
                except Exception as e:
                    failed_mappings += 1
                    error_msg = f"Failed to map part {part_analysis['part_index']}: {str(e)}"
                    state["warnings"].append(error_msg)
                    
                    state["processing_logs"].append({
                        "step": "mapping",
                        "timestamp": datetime.utcnow().isoformat(),
                        "message": error_msg,
                        "level": "warning"
                    })
            
            # Cập nhật state
            state["mapped_data"] = mapped_data
            state["progress_percentage"] = 75.0
            
            # Cập nhật quality metrics
            state["quality_metrics"]["successfully_mapped"] = successfully_mapped
            state["quality_metrics"]["failed_mappings"] = failed_mappings
            
            # Log thành công
            state["processing_logs"].append({
                "step": "mapping",
                "timestamp": datetime.utcnow().isoformat(),
                "message": f"Mapping completed. {successfully_mapped} parts mapped successfully, {failed_mappings} failed",
                "level": "info"
            })
            
            logger.info(f"Mapping node completed for process {state['migrate_process_id']}")
            
        except Exception as e:
            error_msg = f"Error in mapping_node: {str(e)}"
            logger.error(error_msg)
            state["errors"].append(error_msg)
            state["status"] = MigrationStatus.FAILED
            
            state["processing_logs"].append({
                "step": "mapping",
                "timestamp": datetime.utcnow().isoformat(),
                "message": error_msg,
                "level": "error"
            })
        
        return state
    
    @staticmethod
    def validation_node(state: MigrationState) -> MigrationState:
        """
        Node 3: Kiểm tra chất lượng dữ liệu đã mapping
        """
        logger.info(f"Starting validation_node for process {state['migrate_process_id']}")
        
        try:
            state["status"] = MigrationStatus.VALIDATING
            state["current_step"] = "validation"
            state["progress_percentage"] = 85.0
            
            # Log bắt đầu
            state["processing_logs"].append({
                "step": "validation",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Starting data validation",
                "level": "info"
            })
            
            mapped_data = state["mapped_data"]
            validation_errors = []
            
            # Validate quiz structure
            quiz = mapped_data.get("quiz", {})
            if not quiz.get("title"):
                validation_errors.append("Quiz title is missing")
            if not quiz.get("type"):
                validation_errors.append("Quiz type is missing")
            if not quiz.get("parts"):
                validation_errors.append("Quiz has no parts")
            
            # Validate parts
            for part_idx, part in enumerate(quiz.get("parts", []), 1):
                if not part.get("title"):
                    validation_errors.append(f"Part {part_idx} title is missing")
                if not part.get("question_sets"):
                    validation_errors.append(f"Part {part_idx} has no question sets")
                
                # Validate question sets
                for qs_idx, question_set in enumerate(part.get("question_sets", []), 1):
                    if not question_set.get("type"):
                        validation_errors.append(f"Part {part_idx}, Question Set {qs_idx} type is missing")
                    if not question_set.get("questions"):
                        validation_errors.append(f"Part {part_idx}, Question Set {qs_idx} has no questions")
            
            # Tính quality score
            total_checks = 10  # Số lượng checks cơ bản
            passed_checks = total_checks - len(validation_errors)
            quality_score = (passed_checks / total_checks) * 100
            
            # Cập nhật state
            validated_data = mapped_data.copy()
            validated_data["validation_metadata"] = {
                "validation_timestamp": datetime.utcnow().isoformat(),
                "validation_errors": validation_errors,
                "quality_score": quality_score,
                "validation_passed": len(validation_errors) == 0
            }
            
            state["validated_data"] = validated_data
            state["progress_percentage"] = 95.0
            
            # Cập nhật quality metrics
            state["quality_metrics"]["validation_errors"] = validation_errors
            state["quality_metrics"]["quality_score"] = quality_score
            
            # Log kết quả
            if validation_errors:
                state["processing_logs"].append({
                    "step": "validation",
                    "timestamp": datetime.utcnow().isoformat(),
                    "message": f"Validation completed with {len(validation_errors)} errors",
                    "level": "warning",
                    "details": {"errors": validation_errors}
                })
            else:
                state["processing_logs"].append({
                    "step": "validation",
                    "timestamp": datetime.utcnow().isoformat(),
                    "message": "Validation completed successfully",
                    "level": "info"
                })
            
            logger.info(f"Validation node completed for process {state['migrate_process_id']}")
            
        except Exception as e:
            error_msg = f"Error in validation_node: {str(e)}"
            logger.error(error_msg)
            state["errors"].append(error_msg)
            state["status"] = MigrationStatus.FAILED
            
            state["processing_logs"].append({
                "step": "validation",
                "timestamp": datetime.utcnow().isoformat(),
                "message": error_msg,
                "level": "error"
            })
        
        return state
    
    @staticmethod
    def save_node(state: MigrationState) -> MigrationState:
        """
        Node 4: Lưu kết quả vào database
        """
        logger.info(f"Starting save_node for process {state['migrate_process_id']}")
        
        try:
            state["status"] = MigrationStatus.SAVING
            state["current_step"] = "saving"
            state["progress_percentage"] = 98.0
            
            # Log bắt đầu
            state["processing_logs"].append({
                "step": "save",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Starting save to database",
                "level": "info"
            })
            
            # Lưu kết quả cuối cùng
            state["final_result"] = state["validated_data"]
            state["status"] = MigrationStatus.COMPLETED
            state["progress_percentage"] = 100.0
            
            # Tính processing time
            processing_time = (datetime.utcnow() - state["started_at"]).total_seconds()
            state["quality_metrics"]["processing_time"] = processing_time
            
            # Log thành công
            state["processing_logs"].append({
                "step": "save",
                "timestamp": datetime.utcnow().isoformat(),
                "message": f"Migration completed successfully in {processing_time:.2f} seconds",
                "level": "info",
                "details": {
                    "processing_time": processing_time,
                    "quality_score": state["quality_metrics"]["quality_score"]
                }
            })
            
            logger.info(f"Save node completed for process {state['migrate_process_id']}")
            
        except Exception as e:
            error_msg = f"Error in save_node: {str(e)}"
            logger.error(error_msg)
            state["errors"].append(error_msg)
            state["status"] = MigrationStatus.FAILED
            
            state["processing_logs"].append({
                "step": "save",
                "timestamp": datetime.utcnow().isoformat(),
                "message": error_msg,
                "level": "error"
            })
        
        return state
    
    @staticmethod
    def _detect_question_type(question: Dict[str, Any]) -> str:
        """
        Phát hiện loại question từ cấu trúc dữ liệu
        """
        # Logic phát hiện question type (simplified)
        if question.get("type") == "GAP_FILLING":
            return "GAP_FILLING"
        elif question.get("type") == "TRUE_FALSE":
            return "SINGLE_SELECTION"
        elif question.get("type") == "MATCHING_INFO":
            return "MATCHING"
        elif question.get("type") == "FILL_BLANK":
            return "NOTE_COMPLETION"
        elif question.get("mutilple_choice"):
            return "MULTIPLE_CHOICE_MANY"
        elif question.get("single_choice_radio"):
            return "SINGLE_CHOICE"
        else:
            return "UNKNOWN"
    
    @staticmethod
    def _map_part(part_analysis: Dict[str, Any], original_part: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mapping một part từ cấu trúc cũ sang mới
        """
        # Simplified mapping logic - sẽ implement chi tiết sau
        mapped_part = {
            "title": part_analysis["title"],
            "description": part_analysis.get("description"),
            "order": part_analysis["part_index"],
            "question_sets": []
        }
        
        # Group questions by type để tạo question_sets
        questions_by_type = {}
        for question in original_part.get("questions", []):
            q_type = MigrationNodes._detect_question_type(question)
            if q_type not in questions_by_type:
                questions_by_type[q_type] = []
            questions_by_type[q_type].append(question)
        
        # Tạo question_sets
        for q_type, questions in questions_by_type.items():
            question_set = {
                "type": q_type,
                "content": "",  # Sẽ được xử lý chi tiết sau
                "questions": [],
                "options": [],
                "order": len(mapped_part["question_sets"]) + 1
            }
            
            # Simplified question mapping
            for question in questions:
                mapped_question = {
                    "content": question.get("question", ""),
                    "order": len(question_set["questions"]) + 1
                }
                question_set["questions"].append(mapped_question)
            
            mapped_part["question_sets"].append(question_set)
        
        return mapped_part 