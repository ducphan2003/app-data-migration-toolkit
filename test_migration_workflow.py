#!/usr/bin/env python3
"""
Test script cho LangGraph Migration Workflow
"""

import asyncio
import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock data để test
SAMPLE_INPUT_DATA = {
    "id": "test_quiz_001",
    "title": "IELTS Reading Practice Test 1",
    "description": "Practice test for IELTS Reading section",
    "time": 60,  # minutes
    "type": 1,   # reading
    "parts": [
        {
            "title": "Part 1: Reading Passage",
            "description": "Read the passage and answer questions",
            "questions": [
                {
                    "id": "q1",
                    "type": "GAP_FILLING",
                    "question": "Complete the sentences with words from the passage. Use NO MORE THAN TWO WORDS for each answer.",
                    "content": "The research shows that {[A][1]} is important for learning.",
                    "answer": "active participation"
                },
                {
                    "id": "q2", 
                    "type": "TRUE_FALSE",
                    "question": "The study was conducted over a period of five years.",
                    "selection_option": [
                        {"text": "TRUE", "option": "TRUE", "is_correct": True},
                        {"text": "FALSE", "option": "FALSE", "is_correct": False}
                    ]
                }
            ]
        }
    ]
}

async def test_migration_workflow():
    """
    Test LangGraph migration workflow
    """
    try:
        logger.info("Starting migration workflow test...")
        
        # Import sau khi setup logging
        from app.services.migration_workflow import MigrationWorkflow
        from app.repositories.migrate_repository import MigrateRepository
        from app.schemas.migration_state import MigrationState, MigrationStatus
        
        # Mock repository (trong thực tế sẽ connect database)
        class MockMigrateRepository:
            def update_prepare_data_result(self, process_id, result):
                logger.info(f"Mock: Updated prepare data result for process {process_id}")
                
            def update_mapping_structure_result(self, process_id, result):
                logger.info(f"Mock: Updated mapping structure result for process {process_id}")
                
            def update_validate_data_result(self, process_id, result):
                logger.info(f"Mock: Updated validate data result for process {process_id}")
                
            def update_final_result(self, process_id, result):
                logger.info(f"Mock: Updated final result for process {process_id}")
                
            def update_error(self, process_id, error):
                logger.error(f"Mock: Updated error for process {process_id}: {error}")
                
            def get_migrate_process_by_id(self, process_id):
                class MockProcess:
                    def to_dict(self):
                        return {"id": process_id, "status": "processing"}
                return MockProcess()
        
        # Tạo workflow
        mock_repo = MockMigrateRepository()
        workflow = MigrationWorkflow(mock_repo)
        
        # Test parameters
        migrate_process_id = 12345
        user_id = "test_user"
        quiz_type = "reading"
        
        # Chạy workflow
        logger.info("Running migration workflow...")
        final_state = await workflow.run_migration(
            migrate_process_id=migrate_process_id,
            user_id=user_id,
            input_data=SAMPLE_INPUT_DATA,
            quiz_type=quiz_type
        )
        
        # Kiểm tra kết quả
        logger.info("=== MIGRATION WORKFLOW RESULTS ===")
        logger.info(f"Status: {final_state.get('status', 'unknown')}")
        logger.info(f"Progress: {final_state.get('progress_percentage', 0)}%")
        
        quality_metrics = final_state.get('quality_metrics', {})
        logger.info(f"Quality Score: {quality_metrics.get('quality_score', 0)}")
        logger.info(f"Total Questions: {quality_metrics.get('total_questions', 0)}")
        logger.info(f"Successfully Mapped: {quality_metrics.get('successfully_mapped', 0)}")
        logger.info(f"Failed Mappings: {quality_metrics.get('failed_mappings', 0)}")
        logger.info(f"Processing Time: {quality_metrics.get('processing_time', 0):.2f}s")
        
        errors = final_state.get('errors', [])
        if errors:
            logger.error(f"Errors: {errors}")
            
        warnings = final_state.get('warnings', [])
        if warnings:
            logger.warning(f"Warnings: {warnings}")
        
        # In ra processing logs
        logger.info("=== PROCESSING LOGS ===")
        processing_logs = final_state.get('processing_logs', [])
        for log_entry in processing_logs:
            level = log_entry.get('level', 'info').upper()
            timestamp = log_entry.get('timestamp', 'unknown')
            message = log_entry.get('message', 'no message')
            logger.info(f"[{level}] {timestamp}: {message}")
        
        # In ra final result (nếu có)
        final_result = final_state.get('final_result')
        if final_result:
            logger.info("=== FINAL RESULT STRUCTURE ===")
            quiz_data = final_result.get('quiz', {})
            logger.info(f"Quiz Title: {quiz_data.get('title', 'unknown')}")
            logger.info(f"Quiz Type: {quiz_data.get('type', 'unknown')}")
            
            parts = quiz_data.get('parts', [])
            logger.info(f"Total Parts: {len(parts)}")
            
            for i, part in enumerate(parts, 1):
                logger.info(f"  Part {i}: {part.get('title', 'unknown')}")
                question_sets = part.get('question_sets', [])
                logger.info(f"    Question Sets: {len(question_sets)}")
                for j, qs in enumerate(question_sets, 1):
                    questions = qs.get('questions', [])
                    logger.info(f"      QS {j}: {qs.get('type', 'unknown')} ({len(questions)} questions)")
        
        logger.info("Migration workflow test completed successfully!")
        return final_state
        
    except Exception as e:
        logger.error(f"Error in migration workflow test: {str(e)}")
        raise

def main():
    """
    Main function để chạy test
    """
    try:
        # Chạy async test
        result = asyncio.run(test_migration_workflow())
        
        print("\n" + "="*50)
        print("MIGRATION WORKFLOW TEST COMPLETED")
        print("="*50)
        
        status = result.get('status', 'unknown')
        quality_metrics = result.get('quality_metrics', {})
        
        print(f"Final Status: {status}")
        print(f"Quality Score: {quality_metrics.get('quality_score', 0)}")
        print(f"Processing Time: {quality_metrics.get('processing_time', 0):.2f}s")
        
        if status == 'completed':
            print("✅ Test PASSED!")
        else:
            print("❌ Test FAILED!")
            
    except Exception as e:
        print(f"❌ Test FAILED with error: {str(e)}")

if __name__ == "__main__":
    main() 