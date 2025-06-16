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
        logger.info(f"Status: {final_state['status']}")
        logger.info(f"Progress: {final_state['progress_percentage']}%")
        logger.info(f"Quality Score: {final_state['quality_metrics']['quality_score']}")
        logger.info(f"Total Questions: {final_state['quality_metrics']['total_questions']}")
        logger.info(f"Successfully Mapped: {final_state['quality_metrics']['successfully_mapped']}")
        logger.info(f"Failed Mappings: {final_state['quality_metrics']['failed_mappings']}")
        logger.info(f"Processing Time: {final_state['quality_metrics']['processing_time']:.2f}s")
        
        if final_state['errors']:
            logger.error(f"Errors: {final_state['errors']}")
            
        if final_state['warnings']:
            logger.warning(f"Warnings: {final_state['warnings']}")
        
        # In ra processing logs
        logger.info("=== PROCESSING LOGS ===")
        for log_entry in final_state['processing_logs']:
            level = log_entry['level'].upper()
            timestamp = log_entry['timestamp']
            message = log_entry['message']
            logger.info(f"[{level}] {timestamp}: {message}")
        
        # In ra final result (nếu có)
        if final_state['final_result']:
            logger.info("=== FINAL RESULT STRUCTURE ===")
            quiz_data = final_state['final_result']['quiz']
            logger.info(f"Quiz Title: {quiz_data['title']}")
            logger.info(f"Quiz Type: {quiz_data['type']}")
            logger.info(f"Total Parts: {len(quiz_data['parts'])}")
            
            for i, part in enumerate(quiz_data['parts'], 1):
                logger.info(f"  Part {i}: {part['title']}")
                logger.info(f"    Question Sets: {len(part['question_sets'])}")
                for j, qs in enumerate(part['question_sets'], 1):
                    logger.info(f"      QS {j}: {qs['type']} ({len(qs['questions'])} questions)")
        
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
        print(f"Final Status: {result['status']}")
        print(f"Quality Score: {result['quality_metrics']['quality_score']}")
        print(f"Processing Time: {result['quality_metrics']['processing_time']:.2f}s")
        
        if result['status'] == 'completed':
            print("✅ Test PASSED!")
        else:
            print("❌ Test FAILED!")
            
    except Exception as e:
        print(f"❌ Test FAILED with error: {str(e)}")

if __name__ == "__main__":
    main() 