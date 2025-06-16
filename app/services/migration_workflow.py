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
        if state["status"] == MigrationStatus.FAILED:
            if state["retry_count"] < state["max_retries"]:
                state["retry_count"] += 1
                return "retry"
            else:
                return "error"
        
        if state["analyzed_data"] is None:
            return "error"
            
        return "continue"
    
    def _should_continue_after_mapping(self, state: MigrationState) -> Literal["continue", "retry", "error"]:
        """
        Quyết định bước tiếp theo sau mapping node
        """
        if state["status"] == MigrationStatus.FAILED:
            if state["retry_count"] < state["max_retries"]:
                state["retry_count"] += 1
                return "retry"
            else:
                return "error"
        
        if state["mapped_data"] is None:
            return "error"
            
        # Kiểm tra quality threshold
        if state["quality_metrics"]["failed_mappings"] > 0:
            failed_ratio = state["quality_metrics"]["failed_mappings"] / state["total_parts"]
            if failed_ratio > 0.5:  # Nếu quá 50% parts failed
                return "error"
        
        return "continue"
    
    def _should_continue_after_validation(self, state: MigrationState) -> Literal["continue", "retry", "error"]:
        """
        Quyết định bước tiếp theo sau validation node
        """
        if state["status"] == MigrationStatus.FAILED:
            if state["retry_count"] < state["max_retries"]:
                state["retry_count"] += 1
                return "retry"
            else:
                return "error"
        
        if state["validated_data"] is None:
            return "error"
            
        # Kiểm tra quality score
        quality_threshold = state["config"].get("quality_threshold", 80.0)
        if state["quality_metrics"]["quality_score"] < quality_threshold:
            max_errors = state["config"].get("max_validation_errors", 5)
            if len(state["quality_metrics"]["validation_errors"]) > max_errors:
                return "error"
        
        return "continue"
    
    def _should_continue_after_save(self, state: MigrationState) -> Literal["end", "retry", "error"]:
        """
        Quyết định bước tiếp theo sau save node
        """
        if state["status"] == MigrationStatus.FAILED:
            if state["retry_count"] < state["max_retries"]:
                state["retry_count"] += 1
                return "retry"
            else:
                return "error"
        
        if state["status"] == MigrationStatus.COMPLETED:
            return "end"
            
        return "error"
    
    def _error_handler_node(self, state: MigrationState) -> MigrationState:
        """
        Node xử lý lỗi cuối cùng
        """
        logger.error(f"Migration failed for process {state['migrate_process_id']}")
        
        state["status"] = MigrationStatus.FAILED
        state["current_step"] = "error_handling"
        
        # Log lỗi cuối cùng
        state["processing_logs"].append({
            "step": "error_handling",
            "timestamp": datetime.utcnow().isoformat(),
            "message": f"Migration failed after {state['retry_count']} retries",
            "level": "error",
            "details": {
                "errors": state["errors"],
                "warnings": state["warnings"],
                "retry_count": state["retry_count"]
            }
        })
        
        return state
    
    async def _update_database_progress(self, state: MigrationState) -> None:
        """
        Cập nhật tiến độ vào database
        """
        try:
            migrate_process_id = state["migrate_process_id"]
            current_step = state["current_step"]
            
            # Cập nhật theo từng step
            if current_step == "analyze" and state.get("analyzed_data"):
                self.migrate_repo.update_prepare_data_result(
                    migrate_process_id, 
                    state["analyzed_data"]
                )
            
            elif current_step == "mapping" and state.get("mapped_data"):
                self.migrate_repo.update_mapping_structure_result(
                    migrate_process_id, 
                    state["mapped_data"]
                )
            
            elif current_step == "validation" and state.get("validated_data"):
                validation_result = {
                    "status": "success" if state["status"] != MigrationStatus.FAILED else "failed",
                    "quality_score": state["quality_metrics"]["quality_score"],
                    "validation_errors": state["quality_metrics"]["validation_errors"],
                    "processing_logs": state["processing_logs"]
                }
                self.migrate_repo.update_validate_data_result(
                    migrate_process_id, 
                    validation_result
                )
            
            elif current_step == "saving" and state.get("final_result"):
                self.migrate_repo.update_final_result(
                    migrate_process_id, 
                    state["final_result"]
                )
            
            elif state["status"] == MigrationStatus.FAILED:
                error_details = {
                    "errors": state["errors"],
                    "warnings": state["warnings"],
                    "processing_logs": state["processing_logs"],
                    "quality_metrics": state["quality_metrics"]
                }
                self.migrate_repo.update_error(
                    migrate_process_id, 
                    f"Migration failed: {'; '.join(state['errors'])}"
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