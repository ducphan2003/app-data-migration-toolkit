from typing import Dict, Any, Optional
import threading
import logging
import asyncio
from datetime import datetime

from app.repositories.migrate_repository import MigrateRepository
from app.utils.exceptions import NotFoundException, ValidationError
from app.services.migration_workflow import MigrationWorkflow

logger = logging.getLogger(__name__)

class MigrateService:
    def __init__(self, migrate_repo: MigrateRepository):
        self.migrate_repo = migrate_repo
        self.migration_workflow = MigrationWorkflow(migrate_repo)

    def create_migrate_process(self, input_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Tạo mới một migrate process và bắt đầu xử lý ngầm
        """
        try:
            # Validate dữ liệu
            self._validate_input_data(input_data)
            
            quiz_id = str(input_data["id"])
            quiz_type = self._determine_quiz_type(input_data)
            
            # Tạo migrate_process record
            migrate_process = self.migrate_repo.create_migrate_process(
                quiz_id=quiz_id,
                user_id=user_id
            )
            
            # Bắt đầu xử lý ngầm trong thread riêng với LangGraph workflow
            thread = threading.Thread(
                target=self._run_migration_workflow,
                args=(migrate_process.id, user_id, input_data, quiz_type)
            )
            thread.daemon = True
            thread.start()
            
            logger.info(f"Created migrate process {migrate_process.id} for quiz {quiz_id}")
            
            return {
                "migrate_process_id": migrate_process.id,
                "status": "processing",
                "quiz_id": quiz_id,
                "quiz_type": quiz_type
            }
            
        except Exception as e:
            logger.error(f"Error creating migrate process: {str(e)}")
            raise e

    def get_migrate_status(self, migrate_process_id: int) -> Dict[str, Any]:
        """
        Lấy thông tin chi tiết về tiến độ migrate từ LangGraph workflow
        """
        migrate_process = self.migrate_repo.get_migrate_process_by_id(migrate_process_id)
        if not migrate_process:
            raise NotFoundException(f"Không tìm thấy migrate process với id {migrate_process_id}")
        
        # Lấy thêm thông tin từ workflow nếu có
        workflow_status = self.migration_workflow.get_workflow_status(migrate_process_id)
        
        # Merge thông tin từ database và workflow
        result = migrate_process.to_dict()
        if "error" not in workflow_status:
            result.update(workflow_status)
        
        return result

    def _validate_input_data(self, input_data: Dict[str, Any]) -> None:
        """
        Validate dữ liệu input trước khi tạo migrate process
        """
        errors = []

        # Validate required fields
        if not input_data.get("id"):
            errors.append("Missing required field: id")
        
        if not input_data.get("title"):
            errors.append("Missing required field: title")
            
        if not input_data.get("parts"):
            errors.append("Missing required field: parts")
        elif not isinstance(input_data["parts"], list) or len(input_data["parts"]) == 0:
            errors.append("Parts must be a non-empty list")

        # Validate parts structure
        for part_idx, part in enumerate(input_data.get("parts", []), 1):
            if not part.get("questions"):
                errors.append(f"Part {part_idx} must have questions")
            elif not isinstance(part["questions"], list) or len(part["questions"]) == 0:
                errors.append(f"Part {part_idx} questions must be a non-empty list")

        if errors:
            raise ValidationError(errors)

    def _determine_quiz_type(self, input_data: Dict[str, Any]) -> str:
        """
        Xác định loại quiz từ input data
        """
        quiz_type = input_data.get("type")
        
        if quiz_type == 1:
            return "reading"
        elif quiz_type == 2:
            return "listening"
        else:
            # Fallback: check if has listening field
            if input_data.get("listening"):
                return "listening"
            else:
                return "reading"

    def _run_migration_workflow(self, migrate_process_id: int, user_id: str, input_data: Dict[str, Any], quiz_type: str):
        """
        Chạy LangGraph migration workflow trong background thread
        """
        try:
            logger.info(f"Starting LangGraph migration workflow for process {migrate_process_id}")
            
            # Chạy async workflow trong thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                final_state = loop.run_until_complete(
                    self.migration_workflow.run_migration(
                        migrate_process_id, user_id, input_data, quiz_type
                    )
                )
                
                logger.info(f"LangGraph migration workflow completed for process {migrate_process_id}")
                
                # Extract actual state from the LangGraph wrapper
                actual_final_state = self.migration_workflow._extract_actual_state(final_state)

                # Safely extract status from final_state
                try:
                    # Sử dụng actual_final_state thay vì final_state trực tiếp
                    status = actual_final_state.get('status', 'unknown')
                    
                    # Convert enum to string if needed
                    if hasattr(status, 'value'):
                        status = status.value
                    
                    quality_metrics = actual_final_state.get('quality_metrics', {})
                    quality_score = quality_metrics.get('quality_score', 0.0) if isinstance(quality_metrics, dict) else 0.0
                    
                    logger.info(f"Final status: {status}")
                    logger.info(f"Quality score: {quality_score}")
                except Exception as access_error:
                    logger.warning(f"Error accessing final_state fields: {str(access_error)}")
                    logger.info(f"Final state type: {type(final_state)}")
                    logger.info(f"Final state keys: {list(final_state.keys()) if hasattr(final_state, 'keys') else 'N/A'}")
                
            finally:
                loop.close()
            
        except Exception as e:
            logger.error(f"Error in LangGraph migration workflow {migrate_process_id}: {str(e)}")
            self.migrate_repo.update_error(migrate_process_id, str(e))

 