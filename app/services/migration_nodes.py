import logging
import json
import asyncio
from typing import Dict, Any, List
from datetime import datetime
import time

from app.schemas.migration_state import MigrationState, MigrationStatus, QualityMetrics
from app.services.ai_migration_agents import AIMigrationAgents

logger = logging.getLogger(__name__)

class MigrationNodes:
    """Các Node xử lý trong LangGraph migration workflow sử dụng AI agents"""
    
    def __init__(self, 
                 openrouter_api_key: str = None,
                 gpt_api_key: str = None, 
                 gemini_api_key: str = None,
                 claude_api_key: str = None):
        self.ai_agents = AIMigrationAgents(
            openrouter_api_key=openrouter_api_key,
            gpt_api_key=gpt_api_key,
            gemini_api_key=gemini_api_key,
            claude_api_key=claude_api_key
        )
    
    async def analyze_node(self, state: MigrationState) -> MigrationState:
        """
        Node 1: Phân tích cấu trúc dữ liệu đầu vào sử dụng AI
        """
        logger.info(f"Starting AI analyze_node for process {state['migrate_process_id']}")
        
        try:
            state["status"] = MigrationStatus.ANALYZING
            state["current_step"] = "analyze"
            state["progress_percentage"] = 10.0
            
            # Log bắt đầu
            state["processing_logs"].append({
                "step": "analyze",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Starting AI-powered data analysis",
                "level": "info"
            })
            
            input_data = state["raw_input_data"]
            quiz_type = state["quiz_type"]
            
            # Phân tích cấu trúc cơ bản
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
                "ai_question_analyses": [],
                "metadata": {
                    "total_parts": len(input_data.get("parts", [])),
                    "total_questions": 0,
                    "question_types_found": set(),
                    "analysis_timestamp": datetime.utcnow().isoformat(),
                    "ai_powered": True
                }
            }
            
            # Phân tích từng part với AI
            total_questions = 0
            question_types = set()
            
            for part_idx, part in enumerate(input_data.get("parts", []), 1):
                part_questions = part.get("questions", [])
                
                # Sử dụng AI để phân tích loại câu hỏi
                if part_questions:
                    ai_analyses = await self.ai_agents.analyze_question_types(part_questions)
                    
                    part_analysis = {
                        "part_index": part_idx,
                        "title": part.get("title", f"Part {part_idx}"),
                        "description": part.get("description"),
                        "content": part.get("content", ""),
                        "questions_count": len(part_questions),
                        "ai_question_analyses": ai_analyses,
                        "question_types": list(set([analysis.detected_type for analysis in ai_analyses]))
                    }
                    
                    # Cập nhật tổng số
                    total_questions += len(part_questions)
                    for analysis in ai_analyses:
                        question_types.add(analysis.detected_type)
                    
                    analyzed_data["ai_question_analyses"].extend(ai_analyses)
                else:
                    part_analysis = {
                        "part_index": part_idx,
                        "title": part.get("title", f"Part {part_idx}"),
                        "description": part.get("description"),
                        "content": part.get("content", ""),
                        "questions_count": 0,
                        "ai_question_analyses": [],
                        "question_types": []
                    }
                
                analyzed_data["parts_analysis"].append(part_analysis)
                
                # Log progress
                state["processing_logs"].append({
                    "step": "analyze",
                    "timestamp": datetime.utcnow().isoformat(),
                    "message": f"AI analyzed part {part_idx}: found {len(part_questions)} questions",
                    "level": "info",
                    "details": {
                        "part_index": part_idx,
                        "questions_count": len(part_questions),
                        "detected_types": part_analysis["question_types"]
                    }
                })
            
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
                "message": f"AI analysis completed. Found {total_questions} questions in {len(analyzed_data['parts_analysis'])} parts",
                "level": "info",
                "details": {
                    "total_questions": total_questions,
                    "question_types": list(question_types),
                    "ai_confidence_avg": sum([analysis.confidence for analysis in analyzed_data["ai_question_analyses"]]) / len(analyzed_data["ai_question_analyses"]) if analyzed_data["ai_question_analyses"] else 0
                }
            })
            
            logger.info(f"AI Analyze node completed for process {state['migrate_process_id']}")
            
        except Exception as e:
            error_msg = f"Error in AI analyze_node: {str(e)}"
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
    
    async def mapping_node(self, state: MigrationState) -> MigrationState:
        """
        Node 2: Áp dụng AI để chuyển đổi dữ liệu sử dụng modular approach
        """
        logger.info(f"Starting AI mapping_node for process {state['migrate_process_id']}")
        
        try:
            state["status"] = MigrationStatus.MAPPING
            state["current_step"] = "mapping"
            state["progress_percentage"] = 50.0
            
            # Log bắt đầu
            state["processing_logs"].append({
                "step": "mapping",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Starting AI-powered modular data mapping",
                "level": "info"
            })
            
            raw_input_data = state["raw_input_data"]
            analyzed_data = state["analyzed_data"]
            
            # Xử lý từng part với modular approach
            mapped_data = {
                "quiz": None,
                "metadata": {
                    "migration_timestamp": datetime.utcnow().isoformat(),
                    "ai_powered": True,
                    "modular_approach": True
                }
            }
            
            total_question_sets = 0
            total_questions = 0
            
            # Chuẩn bị tasks để xử lý song song các parts
            async def process_part(part_idx: int, part_analysis: Dict[str, Any]) -> Dict[str, Any]:
                """Xử lý một part và trả về kết quả"""
                try:
                    # Lấy part data từ raw input
                    part_data = raw_input_data["parts"][part_idx]
                    
                    # Prepare full part data với quiz info
                    full_part_data = {
                        **raw_input_data,  # Include quiz-level fields
                        **part_data        # Include part-specific fields
                    }
                    
                    # Lấy question analyses cho part này
                    part_question_analyses = part_analysis["ai_question_analyses"]
                    
                    # Sử dụng AI modular transformation
                    logger.info(f"Transforming part {part_idx + 1} with {len(part_question_analyses)} questions (parallel processing)")
                    
                    migration_result = await self.ai_agents.transform_to_question_sets_by_type(
                        full_part_data, 
                        part_question_analyses
                    )
                    
                    return {
                        "part_idx": part_idx,
                        "migration_result": migration_result,
                        "question_analyses_count": len(part_question_analyses)
                    }
                    
                except Exception as e:
                    logger.error(f"Error processing part {part_idx + 1}: {str(e)}")
                    return {
                        "part_idx": part_idx,
                        "migration_result": None,
                        "error": str(e),
                        "question_analyses_count": 0
                    }
            
            # Tạo tasks cho tất cả parts
            part_tasks = [
                process_part(part_idx, part_analysis) 
                for part_idx, part_analysis in enumerate(analyzed_data["parts_analysis"])
            ]
            
            # Chạy song song tất cả parts
            logger.info(f"Starting parallel processing of {len(part_tasks)} parts")
            part_results = await asyncio.gather(*part_tasks, return_exceptions=True)
            
            # Xử lý kết quả theo thứ tự part_idx để đảm bảo thứ tự đúng
            sorted_results = sorted(
                [result for result in part_results if isinstance(result, dict) and not isinstance(result, Exception)],
                key=lambda x: x["part_idx"]
            )
            
            # Set quiz data từ part đầu tiên
            if sorted_results:
                first_result = sorted_results[0]
                if first_result["migration_result"] and first_result["migration_result"].get("quiz"):
                    quiz_data = first_result["migration_result"]["quiz"]
                    mapped_data["quiz"] = {
                        "id": raw_input_data.get("id", 1),  # Sử dụng ID từ input hoặc default 1
                        "title": quiz_data.get("title", raw_input_data.get("title")),
                        "description": quiz_data.get("description"),
                        "status": "published",
                        "type": 1 if analyzed_data["quiz_info"]["type"] == "reading" else 2,
                        "time": raw_input_data.get("time", 60),
                        "vote_count": 0,
                        "total_submitted": 0,
                        "user_created": "system",
                        "date_created": datetime.utcnow().isoformat(),
                        "quiz_type": 4,
                        "mode": 0,
                        "is_test": True,
                        "parts": []  # Initialize parts array in quiz
                    }
            
            # Xử lý kết quả từ tất cả parts
            successful_parts = 0
            failed_parts = 0
            
            for result in sorted_results:
                part_idx = result["part_idx"]
                migration_result = result["migration_result"]
                
                if migration_result and migration_result.get("quiz"):
                    quiz_data = migration_result["quiz"]
                    
                    # Add parts data to quiz.parts (nested structure)
                    transformed_parts = quiz_data.get("parts", [])
                    for transformed_part in transformed_parts:
                        # Count question sets and questions
                        part_question_sets = transformed_part.get("question_sets", [])
                        total_question_sets += len(part_question_sets)
                        
                        for qs in part_question_sets:
                            total_questions += len(qs.get("questions", []))
                        
                        # Add part to quiz.parts instead of mapped_data.parts
                        mapped_data["quiz"]["parts"].append(transformed_part)
                    
                    successful_parts += 1
                    
                    # Log success
                    state["processing_logs"].append({
                        "step": "mapping",
                        "timestamp": datetime.utcnow().isoformat(),
                        "message": f"AI transformed part {part_idx + 1} using parallel modular approach",
                        "level": "info",
                        "details": {
                            "part_index": part_idx + 1,
                            "question_analyses_count": result["question_analyses_count"],
                            "transformation_method": "parallel_modular_by_type",
                            "processing_mode": "parallel"
                        }
                    })
                else:
                    failed_parts += 1
                    error_msg = result.get("error", "Unknown error")
                    
                    # Log error
                    state["processing_logs"].append({
                        "step": "mapping",
                        "timestamp": datetime.utcnow().isoformat(),
                        "message": f"Failed to transform part {part_idx + 1}: {error_msg}",
                        "level": "error",
                        "details": {
                            "part_index": part_idx + 1,
                            "error": error_msg,
                            "processing_mode": "parallel"
                        }
                    })
            
            # Log tổng kết parallel processing
            state["processing_logs"].append({
                "step": "mapping",
                "timestamp": datetime.utcnow().isoformat(),
                "message": f"Parallel processing completed: {successful_parts} successful, {failed_parts} failed parts",
                "level": "info",
                "details": {
                    "total_parts": len(part_tasks),
                    "successful_parts": successful_parts,
                    "failed_parts": failed_parts,
                    "processing_mode": "parallel",
                    "performance_improvement": "enabled"
                }
            })
            
            # Cập nhật state
            state["mapped_data"] = mapped_data
            state["progress_percentage"] = 75.0
            
            # Log thành công
            total_parts = len(mapped_data.get("quiz", {}).get("parts", [])) if mapped_data.get("quiz") else 0
            state["processing_logs"].append({
                "step": "mapping",
                "timestamp": datetime.utcnow().isoformat(),
                "message": f"AI modular mapping completed. Generated {total_question_sets} question sets with {total_questions} questions",
                "level": "info",
                "details": {
                    "total_parts": total_parts,
                    "total_question_sets": total_question_sets,
                    "total_questions": total_questions,
                    "modular_approach": True
                }
            })
            
            logger.info(f"AI Mapping node completed for process {state['migrate_process_id']}")
            
        except Exception as e:
            error_msg = f"Error in AI mapping_node: {str(e)}"
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
    
    async def validation_node(self, state: MigrationState) -> MigrationState:
        """
        Node 3: Validation dữ liệu đã được transform bởi modular approach
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
                "message": "Starting validation of modular migration results",
                "level": "info"
            })
            
            mapped_data = state["mapped_data"]
            
            # Sử dụng kết quả từ modular approach
            final_data = mapped_data
            
            # Debug logs để kiểm tra cấu trúc
            logger.debug(f"Debug - mapped_data keys: {list(mapped_data.keys()) if mapped_data else 'None'}")
            if mapped_data:
                quiz_data = mapped_data.get("quiz")
                logger.debug(f"Debug - quiz_data type: {type(quiz_data)}")
                logger.debug(f"Debug - quiz_data keys: {list(quiz_data.keys()) if quiz_data and isinstance(quiz_data, dict) else 'N/A'}")
                if quiz_data and isinstance(quiz_data, dict):
                    parts_data = quiz_data.get("parts")
                    logger.debug(f"Debug - parts_data type: {type(parts_data)}")
                    logger.debug(f"Debug - parts_data length: {len(parts_data) if isinstance(parts_data, list) else 'N/A'}")
            
            # Loại bỏ questions từ parts vì chúng đã nằm trong question_sets
            quiz_data = final_data.get("quiz", {})
            if quiz_data and "parts" in quiz_data:
                for part in quiz_data["parts"]:
                    # Xóa questions field khỏi part vì questions đã nằm trong question_sets
                    if "questions" in part:
                        del part["questions"]
                        logger.debug(f"Removed questions field from part {part.get('id', 'unknown')}")
            
            # Tạo final_result với cấu trúc đúng
            final_result = final_data
            
            # Validation checks
            validation_errors = []
            validation_warnings = []
            
            # Kiểm tra cấu trúc cơ bản
            if not final_result.get("quiz", {}).get("title"):
                validation_errors.append("Quiz title is missing")
            
            if not final_result.get("quiz", {}).get("parts"):
                validation_errors.append("No parts found in quiz")
            
            # Kiểm tra từng part
            for part in final_result.get("quiz", {}).get("parts", []):
                if not part.get("title"):
                    validation_warnings.append(f"Part {part.get('sort', 'unknown')} has no title")
                
                if not part.get("question_sets"):
                    validation_warnings.append(f"Part {part.get('sort', 'unknown')} has no question sets")
                
                # Đảm bảo part không có questions field (đã được moved vào question_sets)
                if "questions" in part:
                    validation_warnings.append(f"Part {part.get('sort', 'unknown')} still contains questions field - should be in question_sets")
                
                # Kiểm tra question sets
                for qs in part.get("question_sets", []):
                    if not qs.get("question_type"):
                        validation_errors.append(f"Question set in part {part.get('sort', 'unknown')} has no question_type")
                    
                    if not qs.get("questions"):
                        validation_warnings.append(f"Question set {qs.get('sort', 'unknown')} in part {part.get('sort', 'unknown')} has no questions")
            
            # Cập nhật state
            state["validated_data"] = final_result  # Sử dụng final_result với cấu trúc đúng
            state["final_result"] = final_result    # Lưu final_result với cấu trúc đúng
            state["validation_errors"] = validation_errors
            state["validation_warnings"] = validation_warnings
            state["progress_percentage"] = 95.0
            
            # Cập nhật quality metrics
            state["quality_metrics"]["validation_errors"] = validation_errors
            state["quality_metrics"]["validation_warnings"] = validation_warnings
            state["quality_metrics"]["ai_enhanced"] = True
            
            # Determine status
            if validation_errors:
                state["status"] = MigrationStatus.FAILED
                state["errors"].extend(validation_errors)
            else:
                state["status"] = MigrationStatus.COMPLETED
            
            # Log kết quả
            state["processing_logs"].append({
                "step": "validation",
                "timestamp": datetime.utcnow().isoformat(),
                "message": f"Modular validation completed. {len(validation_errors)} errors, {len(validation_warnings)} warnings. Removed questions field from parts.",
                "level": "info" if not validation_errors else "error",
                "details": {
                    "validation_errors": validation_errors,
                    "validation_warnings": validation_warnings,
                    "modular_approach": True,
                    "questions_removed_from_parts": True
                }
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
    
    def save_node(self, state: MigrationState) -> MigrationState:
        """
        Node 4: Lưu kết quả (giữ nguyên logic cũ)
        """
        logger.info(f"Starting save_node for process {state['migrate_process_id']}")
        
        try:
            state["current_step"] = "save"
            state["progress_percentage"] = 100.0
            
            # Log bắt đầu
            state["processing_logs"].append({
                "step": "save",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Starting save process",
                "level": "info"
            })
            
            # Lưu final_result vào file (tạm thời)
            output_file = f"import-data-tool/test-result/final_result_{state['migrate_process_id']}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(state["final_result"], f, ensure_ascii=False, indent=2)
            
            # Cập nhật state
            state["output_file"] = output_file
            state["status"] = MigrationStatus.COMPLETED
            
            # Log thành công
            state["processing_logs"].append({
                "step": "save",
                "timestamp": datetime.utcnow().isoformat(),
                "message": f"Results saved to {output_file}",
                "level": "info"
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