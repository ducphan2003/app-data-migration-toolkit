import logging
from typing import Dict, Any, Literal
from datetime import datetime

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.schemas.migration_state import MigrationState, MigrationStatus, QualityMetrics
from app.services.migration_nodes import MigrationNodes
from app.repositories.migrate_repository import MigrateRepository

logger = logging.getLogger(__name__)

class MigrationWorkflow:
    """LangGraph workflow cho quá trình migration"""
    
    def __init__(self, migrate_repo: MigrateRepository):
        self.migrate_repo = migrate_repo
        self.workflow = self._build_workflow()
        
    def _build_workflow(self) -> StateGraph:
        """
        Xây dựng LangGraph workflow
        """
        # Tạo StateGraph
        workflow = StateGraph(MigrationState)
        
        # Thêm các nodes
        workflow.add_node("analyze", MigrationNodes.analyze_node)
        workflow.add_node("mapping", MigrationNodes.mapping_node)
        workflow.add_node("validation", MigrationNodes.validation_node)
        workflow.add_node("save", MigrationNodes.save_node)
        workflow.add_node("error_handler", self._error_handler_node)
        
        # Định nghĩa entry point
        workflow.set_entry_point("analyze")
        
        # Thêm conditional edges
        workflow.add_conditional_edges(
            "analyze",
            self._should_continue_after_analyze,
            {
                "continue": "mapping",
                "retry": "analyze",
                "error": "error_handler"
            }
        )
        
        workflow.add_conditional_edges(
            "mapping",
            self._should_continue_after_mapping,
            {
                "continue": "validation",
                "retry": "mapping",
                "error": "error_handler"
            }
        )
        
        workflow.add_conditional_edges(
            "validation",
            self._should_continue_after_validation,
            {
                "continue": "save",
                "retry": "validation",
                "error": "error_handler"
            }
        )
        
        workflow.add_conditional_edges(
            "save",
            self._should_continue_after_save,
            {
                "end": END,
                "retry": "save",
                "error": "error_handler"
            }
        )
        
        workflow.add_edge("error_handler", END)
        
        return workflow
    
    def create_initial_state(
        self, 
        migrate_process_id: int, 
        user_id: str, 
        input_data: Dict[str, Any], 
        quiz_type: str
    ) -> MigrationState:
        """
        Tạo initial state cho workflow
        """
        return MigrationState(
            # Process metadata
            migrate_process_id=migrate_process_id,
            user_id=user_id,
            status=MigrationStatus.PENDING,
            current_step="initialize",
            started_at=datetime.utcnow(),
            
            # Input data
            raw_input_data=input_data,
            quiz_type=quiz_type,
            
            # Processing results
            analyzed_data=None,
            mapped_data=None,
            validated_data=None,
            final_result=None,
            
            # Quality tracking
            quality_metrics=QualityMetrics(
                total_questions=0,
                successfully_mapped=0,
                failed_mappings=0,
                validation_errors=[],
                quality_score=0.0,
                processing_time=0.0
            ),
            
            # Error handling
            errors=[],
            warnings=[],
            retry_count=0,
            max_retries=3,
            
            # Progress tracking
            progress_percentage=0.0,
            current_part_index=0,
            total_parts=0,
            
            # Configuration
            config={
                "enable_parallel_processing": True,
                "quality_threshold": 80.0,
                "max_validation_errors": 5
            },
            
            # Logs
            processing_logs=[]
        )
    
    async def run_migration(
        self, 
        migrate_process_id: int, 
        user_id: str, 
        input_data: Dict[str, Any], 
        quiz_type: str
    ) -> MigrationState:
        """
        Chạy migration workflow
        """
        try:
            logger.info(f"Starting migration workflow for process {migrate_process_id}")
            
            # Tạo initial state
            initial_state = self.create_initial_state(
                migrate_process_id, user_id, input_data, quiz_type
            )
            
            # Compile workflow với memory saver
            memory = MemorySaver()
            app = self.workflow.compile(checkpointer=memory)
            
            # Chạy workflow
            config = {"configurable": {"thread_id": str(migrate_process_id)}}
            
            final_state = None
            async for state in app.astream(initial_state, config):
                final_state = state
                
                # Cập nhật database sau mỗi step
                await self._update_database_progress(final_state)
                
                logger.info(f"Migration step completed: {final_state.get('current_step', 'unknown')}")
            
            logger.info(f"Migration workflow completed for process {migrate_process_id}")
            return final_state
            
        except Exception as e:
            error_msg = f"Error in migration workflow: {str(e)}"
            logger.error(error_msg)
            
            # Cập nhật lỗi vào database
            self.migrate_repo.update_error(migrate_process_id, error_msg)
            
            raise e
    
    def _should_continue_after_analyze(self, state: MigrationState) -> Literal["continue", "retry", "error"]:
        """
        Quyết định bước tiếp theo sau analyze node
        """
        actual_state = self._extract_actual_state(state)
        
        if actual_state.get("status") == MigrationStatus.FAILED:
            retry_count = actual_state.get("retry_count", 0)
            max_retries = actual_state.get("max_retries", 3)
            if retry_count < max_retries:
                actual_state["retry_count"] = retry_count + 1
                return "retry"
            else:
                return "error"
        
        if actual_state.get("analyzed_data") is None:
            return "error"
            
        return "continue"
    
    def _should_continue_after_mapping(self, state: MigrationState) -> Literal["continue", "retry", "error"]:
        """
        Quyết định bước tiếp theo sau mapping node
        """
        actual_state = self._extract_actual_state(state)
        
        if actual_state.get("status") == MigrationStatus.FAILED:
            retry_count = actual_state.get("retry_count", 0)
            max_retries = actual_state.get("max_retries", 3)
            if retry_count < max_retries:
                actual_state["retry_count"] = retry_count + 1
                return "retry"
            else:
                return "error"
        
        if actual_state.get("mapped_data") is None:
            return "error"
            
        # Kiểm tra quality threshold
        quality_metrics = actual_state.get("quality_metrics", {})
        failed_mappings = quality_metrics.get("failed_mappings", 0)
        total_parts = actual_state.get("total_parts", 1)
        
        if failed_mappings > 0:
            failed_ratio = failed_mappings / total_parts
            if failed_ratio > 0.5:  # Nếu quá 50% parts failed
                return "error"
        
        return "continue"
    
    def _should_continue_after_validation(self, state: MigrationState) -> Literal["continue", "retry", "error"]:
        """
        Quyết định bước tiếp theo sau validation node
        """
        actual_state = self._extract_actual_state(state)
        
        if actual_state.get("status") == MigrationStatus.FAILED:
            retry_count = actual_state.get("retry_count", 0)
            max_retries = actual_state.get("max_retries", 3)
            if retry_count < max_retries:
                actual_state["retry_count"] = retry_count + 1
                return "retry"
            else:
                return "error"
        
        if actual_state.get("validated_data") is None:
            return "error"
            
        # Kiểm tra quality score
        config = actual_state.get("config", {})
        quality_metrics = actual_state.get("quality_metrics", {})
        
        quality_threshold = config.get("quality_threshold", 80.0)
        quality_score = quality_metrics.get("quality_score", 0.0)
        
        if quality_score < quality_threshold:
            max_errors = config.get("max_validation_errors", 5)
            validation_errors = quality_metrics.get("validation_errors", [])
            if len(validation_errors) > max_errors:
                return "error"
        
        return "continue"
    
    def _should_continue_after_save(self, state: MigrationState) -> Literal["end", "retry", "error"]:
        """
        Quyết định bước tiếp theo sau save node
        """
        actual_state = self._extract_actual_state(state)
        status = actual_state.get("status")
        
        if status == MigrationStatus.FAILED:
            retry_count = actual_state.get("retry_count", 0)
            max_retries = actual_state.get("max_retries", 3)
            if retry_count < max_retries:
                actual_state["retry_count"] = retry_count + 1
                return "retry"
            else:
                return "error"
        
        if status == MigrationStatus.COMPLETED:
            return "end"
            
        return "error"
    
    def _error_handler_node(self, state: MigrationState) -> MigrationState:
        """
        Node xử lý lỗi cuối cùng
        """
        actual_state = self._extract_actual_state(state)
        migrate_process_id = actual_state.get("migrate_process_id", "unknown")
        logger.error(f"Migration failed for process {migrate_process_id}")
        
        actual_state["status"] = MigrationStatus.FAILED
        actual_state["current_step"] = "error_handling"
        
        # Log lỗi cuối cùng
        processing_logs = actual_state.get("processing_logs", [])
        retry_count = actual_state.get("retry_count", 0)
        errors = actual_state.get("errors", [])
        warnings = actual_state.get("warnings", [])
        
        processing_logs.append({
            "step": "error_handling",
            "timestamp": datetime.utcnow().isoformat(),
            "message": f"Migration failed after {retry_count} retries",
            "level": "error",
            "details": {
                "errors": errors,
                "warnings": warnings,
                "retry_count": retry_count
            }
        })
        
        actual_state["processing_logs"] = processing_logs
        
        return state
    
    def _extract_actual_state(self, state: MigrationState) -> Dict[str, Any]:
        """
        Extract actual state từ LangGraph state wrapper
        LangGraph có thể wrap state trong node key như {'validation': {...}}
        """
        # Nếu state có key là node names, extract actual state
        node_keys = ['analyze', 'mapping', 'validation', 'save', 'error_handler']
        
        for key in node_keys:
            if key in state and isinstance(state[key], dict):
                return state[key]
        
        # Nếu không có wrapper, return state as is
        return state
    
    async def _update_database_progress(self, state: MigrationState) -> None:
        """
        Cập nhật tiến độ vào database
        """
        try:
            # Extract actual state từ LangGraph wrapper
            actual_state = self._extract_actual_state(state)
            
            migrate_process_id = actual_state.get("migrate_process_id")
            current_step = actual_state.get("current_step")
            
            if not migrate_process_id:
                logger.warning("migrate_process_id not found in state")
                logger.debug(f"State keys: {list(state.keys())}")
                logger.debug(f"Actual state keys: {list(actual_state.keys())}")
                return
            
            # Cập nhật theo từng step
            if current_step == "analyze" and actual_state.get("analyzed_data"):
                self.migrate_repo.update_prepare_data_result(
                    migrate_process_id, 
                    actual_state.get("analyzed_data")
                )
            
            elif current_step == "mapping" and actual_state.get("mapped_data"):
                self.migrate_repo.update_mapping_structure_result(
                    migrate_process_id, 
                    actual_state.get("mapped_data")
                )
            
            elif current_step == "validation" and actual_state.get("validated_data"):
                quality_metrics = actual_state.get("quality_metrics", {})
                validation_result = {
                    "status": "success" if actual_state.get("status") != MigrationStatus.FAILED else "failed",
                    "quality_score": quality_metrics.get("quality_score", 0.0),
                    "validation_errors": quality_metrics.get("validation_errors", []),
                    "processing_logs": actual_state.get("processing_logs", [])
                }
                self.migrate_repo.update_validate_data_result(
                    migrate_process_id, 
                    validation_result
                )
            
            elif current_step == "saving" and actual_state.get("final_result"):
                self.migrate_repo.update_final_result(
                    migrate_process_id, 
                    actual_state.get("final_result")
                )
            
            elif actual_state.get("status") == MigrationStatus.FAILED:
                error_details = {
                    "errors": actual_state.get("errors", []),
                    "warnings": actual_state.get("warnings", []),
                    "processing_logs": actual_state.get("processing_logs", []),
                    "quality_metrics": actual_state.get("quality_metrics", {})
                }
                errors = actual_state.get("errors", [])
                error_message = f"Migration failed: {'; '.join(errors)}" if errors else "Migration failed"
                self.migrate_repo.update_error(
                    migrate_process_id, 
                    error_message
                )
                
        except Exception as e:
            logger.error(f"Error updating database progress: {str(e)}")
    
    def get_workflow_status(self, migrate_process_id: int) -> Dict[str, Any]:
        """
        Lấy trạng thái workflow từ memory
        """
        try:
            # Implement logic để lấy state từ memory nếu cần
            # Hiện tại return từ database
            return self.migrate_repo.get_migrate_process_by_id(migrate_process_id).to_dict()
        except Exception as e:
            logger.error(f"Error getting workflow status: {str(e)}")
            return {"error": str(e)} 