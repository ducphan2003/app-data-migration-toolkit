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
        Node 2: Áp dụng AI để chuyển đổi dữ liệu
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
                "message": "Starting AI-powered data mapping",
                "level": "info"
            })
            
            analyzed_data = state["analyzed_data"]
            quiz_info = analyzed_data["quiz_info"]
            
            # Tạo cấu trúc quiz cơ bản
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
            
            # Mapping từng part với AI
            successfully_mapped = 0
            failed_mappings = 0
            
            for part_analysis in analyzed_data["parts_analysis"]:
                try:
                    part_idx = part_analysis["part_index"]
                    original_part = state["raw_input_data"]["parts"][part_idx - 1]
                    
                    # Sử dụng AI để chuyển đổi part
                    part_ai_analyses = part_analysis["ai_question_analyses"]
                    if part_ai_analyses:
                        ai_question_sets = await self.ai_agents.transform_to_question_sets(
                            original_part, 
                            part_ai_analyses
                        )
                        
                        # Tạo mapped part
                        mapped_part = {
                            "title": part_analysis["title"],
                            "description": part_analysis["description"] or original_part.get("content", ""),
                            "order": part_idx,
                            "question_sets": []
                        }
                        
                        # Chuyển đổi AI question sets thành format database
                        for order, ai_qs in enumerate(ai_question_sets, 1):
                            question_set = {
                                "type": ai_qs.type,
                                "content": ai_qs.content,
                                "instructions": ai_qs.instructions,
                                "questions": [],
                                "options": ai_qs.options,
                                "order": order,
                                "metadata": ai_qs.metadata
                            }
                            
                            # Chuyển đổi questions
                            for q_order, ai_question in enumerate(ai_qs.questions, 1):
                                question = {
                                    "quiz_id": 0,
                                    "type": "",
                                    "part_id": None,
                                    "content": ai_question.get("content", ""),
                                    "order": q_order
                                }
                                question_set["questions"].append(question)
                            
                            mapped_part["question_sets"].append(question_set)
                        
                        mapped_data["quiz"]["parts"].append(mapped_part)
                        successfully_mapped += 1
                        
                        state["processing_logs"].append({
                            "step": "mapping",
                            "timestamp": datetime.utcnow().isoformat(),
                            "message": f"AI successfully mapped part {part_idx} with {len(ai_question_sets)} question sets",
                            "level": "info",
                            "details": {
                                "part_index": part_idx,
                                "question_sets_count": len(ai_question_sets),
                                "question_types": [qs.type for qs in ai_question_sets]
                            }
                        })
                    else:
                        # Fallback cho part không có questions
                        mapped_part = {
                            "title": part_analysis["title"],
                            "description": part_analysis["description"] or original_part.get("content", ""),
                            "order": part_idx,
                            "question_sets": []
                        }
                        mapped_data["quiz"]["parts"].append(mapped_part)
                        successfully_mapped += 1
                        
                        state["processing_logs"].append({
                            "step": "mapping",
                            "timestamp": datetime.utcnow().isoformat(),
                            "message": f"Mapped part {part_idx} (no questions)",
                            "level": "info"
                        })
                    
                except Exception as e:
                    failed_mappings += 1
                    error_msg = f"Failed to AI map part {part_analysis['part_index']}: {str(e)}"
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
                "message": f"AI mapping completed. Successfully mapped {successfully_mapped} parts, {failed_mappings} failed",
                "level": "info",
                "details": {
                    "successfully_mapped": successfully_mapped,
                    "failed_mappings": failed_mappings
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
        Node 3: Validation và enhancement với AI
        """
        logger.info(f"Starting AI validation_node for process {state['migrate_process_id']}")
        
        try:
            state["status"] = MigrationStatus.VALIDATING
            state["current_step"] = "validation"
            state["progress_percentage"] = 85.0
            
            # Log bắt đầu
            state["processing_logs"].append({
                "step": "validation",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Starting AI-powered validation and enhancement",
                "level": "info"
            })
            
            mapped_data = state["mapped_data"]
            
            # Sử dụng AI để validate và enhance
            enhanced_result = await self.ai_agents.validate_and_enhance(mapped_data)
            
            # Cập nhật với kết quả enhanced
            final_data = {
                "quiz": {
                    "id": "auto_generate",
                    "title": enhanced_result.quiz_title,
                    "description": mapped_data["quiz"]["description"],
                    "status": "published",
                    "type": enhanced_result.quiz_type,
                    "time_limit": mapped_data["quiz"]["time_limit"],
                    "vote_count": 0,
                    "total_submitted": 0,
                    "user_created": "system",
                    "date_created": datetime.utcnow().isoformat(),
                    "parts": []
                }
            }
            
            # Chuyển đổi enhanced parts
            for enhanced_part in enhanced_result.parts:
                final_part = {
                    "title": enhanced_part.title,
                    "description": enhanced_part.description,
                    "order": enhanced_part.order,
                    "question_sets": []
                }
                
                for enhanced_qs in enhanced_part.question_sets:
                    final_qs = {
                        "type": enhanced_qs.type,
                        "content": enhanced_qs.content,
                        "instructions": enhanced_qs.instructions,
                        "questions": [],
                        "options": enhanced_qs.options,
                        "order": len(final_part["question_sets"]) + 1,
                        "metadata": enhanced_qs.metadata
                    }
                    
                    for enhanced_q in enhanced_qs.questions:
                        final_q = {
                            "quiz_id": 0,
                            "type": "",
                            "part_id": None,
                            "content": enhanced_q.get("content", ""),
                            "order": enhanced_q.get("order", 1)
                        }
                        final_qs["questions"].append(final_q)
                    
                    final_part["question_sets"].append(final_qs)
                
                final_data["quiz"]["parts"].append(final_part)
            
            # Validation checks
            validation_errors = []
            validation_warnings = []
            
            # Kiểm tra cấu trúc cơ bản
            if not final_data["quiz"]["title"]:
                validation_errors.append("Quiz title is missing")
            
            if not final_data["quiz"]["parts"]:
                validation_errors.append("No parts found in quiz")
            
            # Kiểm tra từng part
            for part in final_data["quiz"]["parts"]:
                if not part["title"]:
                    validation_warnings.append(f"Part {part['order']} has no title")
                
                if not part["question_sets"]:
                    validation_warnings.append(f"Part {part['order']} has no question sets")
                
                # Kiểm tra question sets
                for qs in part["question_sets"]:
                    if not qs["type"]:
                        validation_errors.append(f"Question set in part {part['order']} has no type")
                    
                    if not qs["questions"]:
                        validation_warnings.append(f"Question set {qs['order']} in part {part['order']} has no questions")
            
            # Cập nhật state
            state["final_result"] = final_data
            state["validation_errors"] = validation_errors
            state["validation_warnings"] = validation_warnings
            state["progress_percentage"] = 95.0
            
            # Cập nhật quality metrics
            state["quality_metrics"]["validation_errors"] = len(validation_errors)
            state["quality_metrics"]["validation_warnings"] = len(validation_warnings)
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
                "message": f"AI validation completed. {len(validation_errors)} errors, {len(validation_warnings)} warnings",
                "level": "info" if not validation_errors else "error",
                "details": {
                    "validation_errors": validation_errors,
                    "validation_warnings": validation_warnings,
                    "ai_metadata": enhanced_result.metadata
                }
            })
            
            logger.info(f"AI Validation node completed for process {state['migrate_process_id']}")
            
        except Exception as e:
            error_msg = f"Error in AI validation_node: {str(e)}"
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