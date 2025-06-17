#!/usr/bin/env python3
"""
Simple test script để debug AI Migration từng bước
"""

import asyncio
import json
import logging
from datetime import datetime

from app.services.ai_migration_agents import AIMigrationAgents
from app.schemas.migration_state import MigrationState, MigrationStatus

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_simple_migration():
    """Test từng bước migration"""
    
    # Load input data
    input_file = "import-data-tool/raw-data/reading.input-fill_blank.json"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_input_data = json.load(f)
        
        logger.info(f"Loaded input data from {input_file}")
        logger.info(f"Quiz title: {raw_input_data.get('title')}")
        logger.info(f"Number of parts: {len(raw_input_data.get('parts', []))}")
        
        # Tạo AI agents (sẽ sử dụng fallback)
        ai_agents = AIMigrationAgents()
        
        # Test step 1: Analyze questions
        logger.info("=== STEP 1: ANALYZE QUESTIONS ===")
        parts = raw_input_data.get('parts', [])
        if parts:
            part = parts[0]
            questions = part.get('questions', [])
            logger.info(f"Found {len(questions)} questions in part 1")
            
            analyses = await ai_agents.analyze_question_types(questions)
            logger.info(f"Analysis result: {len(analyses)} analyses")
            for analysis in analyses:
                logger.info(f"  - Question {analysis.question_id}: {analysis.detected_type}")
            
            # Test step 2: Transform to question sets
            logger.info("=== STEP 2: TRANSFORM TO QUESTION SETS ===")
            question_sets = await ai_agents.transform_to_question_sets(part, analyses)
            logger.info(f"Transform result: {len(question_sets)} question sets")
            for qs in question_sets:
                logger.info(f"  - {qs.type}: {len(qs.questions)} questions")
            
            # Test step 3: Create migration result
            logger.info("=== STEP 3: CREATE MIGRATION RESULT ===")
            migration_result = {
                "quiz_title": raw_input_data.get('title', 'Test Quiz'),
                "quiz_type": "reading",
                "parts": [
                    {
                        "title": part.get('title', 'Part 1'),
                        "description": "Test description",
                        "content": part.get('content', ''),
                        "question_sets": [qs.dict() for qs in question_sets],
                        "order": 1
                    }
                ]
            }
            
            # Test step 4: Validate and enhance
            logger.info("=== STEP 4: VALIDATE AND ENHANCE ===")
            final_result = await ai_agents.validate_and_enhance(migration_result)
            logger.info(f"Validation result type: {type(final_result)}")
            logger.info(f"Final result quiz title: {final_result.quiz_title}")
            logger.info(f"Final result parts: {len(final_result.parts)}")
            
            # Save result
            output_file = f"import-data-tool/test-result/simple_migration_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                result_dict = final_result.dict()
                json.dump(result_dict, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ Simple migration test completed successfully!")
            logger.info(f"Result saved to: {output_file}")
            
            return final_result
        else:
            logger.error("No parts found in input data")
            return None
            
    except Exception as e:
        logger.error(f"Error during simple migration: {str(e)}")
        logger.exception("Full exception details:")
        raise

def main():
    """Main function"""
    logger.info("Starting Simple AI Migration Test")
    
    try:
        result = asyncio.run(test_simple_migration())
        
        if result:
            logger.info("✅ Simple AI Migration test completed successfully!")
        else:
            logger.error("❌ Simple AI Migration test failed - no result returned")
            
    except Exception as e:
        logger.error(f"❌ Simple AI Migration test failed with exception: {str(e)}")
        raise

if __name__ == "__main__":
    main() 