#!/usr/bin/env python3
"""
Test script cho AI Migration Workflow
"""

import asyncio
import json
import logging
import os
from datetime import datetime

from app.services.migration_workflow import run_ai_migration
from config.config import app_config

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def convert_to_serializable(obj):
    """Convert objects to JSON serializable format"""
    try:
        if hasattr(obj, 'dict'):  # Pydantic objects
            return obj.dict()
        elif hasattr(obj, '__dict__'):  # Regular objects
            return obj.__dict__
        elif isinstance(obj, list):
            return [convert_to_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: convert_to_serializable(value) for key, value in obj.items()}
        elif hasattr(obj, 'isoformat'):  # datetime objects
            return obj.isoformat()
        elif hasattr(obj, 'value'):  # Enum objects
            return obj.value
        else:
            return str(obj)
    except Exception as e:
        logger.error(f"Error converting object to serializable: {e}, object type: {type(obj)}")
        return str(obj)

async def test_ai_migration(use_mock_llm=False):
    """Test AI migration với dữ liệu thực"""
    
    # Load input data
    input_file = "import-data-tool/raw-data/reading.input-fill_blank.json"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_input_data = json.load(f)
        
        logger.info(f"Loaded input data from {input_file}")
        logger.info(f"Quiz title: {raw_input_data.get('title')}")
        logger.info(f"Number of parts: {len(raw_input_data.get('parts', []))}")
        
        # Đếm tổng số questions
        total_questions = 0
        for part in raw_input_data.get('parts', []):
            total_questions += len(part.get('questions', []))
        logger.info(f"Total questions: {total_questions}")
        
        # Cấu hình
        quiz_type = "reading"
        migrate_process_id = f"ai_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if use_mock_llm:
            logger.info("Using Mock LLM for fast testing")
            # Force sử dụng Mock LLM bằng cách không truyền API keys
            openrouter_api_key = None
            gpt_api_key = None
            gemini_api_key = None
            claude_api_key = None
        else:
            # Load API keys từ config
            openrouter_api_key = app_config.PROMPT_YOUR_API_OPENROUTER or os.getenv("PROMPT_YOUR_API_OPENROUTER")
            gpt_api_key = app_config.PROMPT_YOUR_API_GPT or os.getenv("PROMPT_YOUR_API_GPT")
            gemini_api_key = app_config.PROMPT_YOUR_API_GEMINI or os.getenv("PROMPT_YOUR_API_GEMINI")
            claude_api_key = app_config.PROMPT_YOUR_API_CLAUDE or os.getenv("PROMPT_YOUR_API_CLAUDE")
            
            # Check available APIs
            available_apis = []
            if openrouter_api_key:
                available_apis.append("OpenRouter")
            if gpt_api_key:
                available_apis.append("GPT")
            if gemini_api_key:
                available_apis.append("Gemini")
            if claude_api_key:
                available_apis.append("Claude")
            
            if available_apis:
                logger.info(f"Available AI APIs: {', '.join(available_apis)}")
            else:
                logger.warning("No AI API keys found. Using Mock LLM for testing.")
        
        logger.info("Starting AI migration...")
        
        # Chạy AI migration
        result = await run_ai_migration(
            raw_input_data=raw_input_data,
            quiz_type=quiz_type,
            migrate_process_id=migrate_process_id,
            openrouter_api_key=openrouter_api_key,
            gpt_api_key=gpt_api_key,
            gemini_api_key=gemini_api_key,
            claude_api_key=claude_api_key
        )
        
        # Log kết quả
        logger.info(f"Migration completed with status: {result['status']}")
        logger.info(f"Progress: {result['progress_percentage']}%")
        logger.info(f"Errors: {len(result['errors'])}")
        logger.info(f"Warnings: {len(result['warnings'])}")
        
        # Debug: print result structure
        logger.debug(f"Result type: {type(result)}")
        logger.debug(f"Result keys: {list(result.keys()) if hasattr(result, 'keys') else 'No keys'}")
        if 'final_result' in result:
            logger.debug(f"Final result type: {type(result['final_result'])}")
            if result['final_result']:
                logger.debug(f"Final result keys: {list(result['final_result'].keys()) if hasattr(result['final_result'], 'keys') else 'No keys'}")
        
        # In quality metrics
        metrics = result['quality_metrics']
        logger.info("Quality Metrics:")
        logger.info(f"  - Total questions: {metrics['total_questions']}")
        logger.info(f"  - Successfully mapped: {metrics['successfully_mapped']}")
        logger.info(f"  - Failed mappings: {metrics['failed_mappings']}")
        logger.info(f"  - Validation errors: {metrics['validation_errors']}")
        logger.info(f"  - Validation warnings: {metrics['validation_warnings']}")
        logger.info(f"  - Processing time: {metrics['processing_time']:.2f}s")
        logger.info(f"  - AI enhanced: {metrics['ai_enhanced']}")
        
        # In processing logs
        logger.info("Processing Logs:")
        for log_entry in result['processing_logs']:
            level = log_entry['level'].upper()
            message = log_entry['message']
            step = log_entry['step']
            logger.info(f"  [{level}] {step}: {message}")
        
        # Lưu kết quả chi tiết
        output_file = f"import-data-tool/test-result/ai_migration_result_{migrate_process_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            # Convert all objects to JSON serializable format
            try:
                logger.debug(f"About to convert result to serializable, result type: {type(result)}")
                logger.debug(f"Result has keys: {list(result.keys()) if hasattr(result, 'keys') else 'No keys method'}")
                
                result_copy = convert_to_serializable(result)
                
                logger.debug(f"Converted result type: {type(result_copy)}")
                logger.debug(f"About to save to JSON...")
                
                json.dump(result_copy, f, ensure_ascii=False, indent=2)
                logger.debug(f"Successfully saved result to {output_file}")
            except Exception as e:
                logger.error(f"Error saving result to JSON: {e}")
                logger.exception("Full exception details:")
                # Save a simple version
                simple_result = {
                    "status": str(result.get('status', 'unknown')),
                    "errors": result.get('errors', []),
                    "warnings": result.get('warnings', []),
                    "processing_logs": result.get('processing_logs', [])
                }
                json.dump(simple_result, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Detailed results saved to: {output_file}")
        
        # Kiểm tra final_result
        if 'final_result' in result and result['final_result']:
            final_result = result['final_result']
            quiz = final_result.get('quiz', {})
            parts = quiz.get('parts', [])
            
            logger.info("Final Result Summary:")
            logger.info(f"  - Quiz title: {quiz.get('title')}")
            logger.info(f"  - Quiz type: {quiz.get('type')}")
            logger.info(f"  - Number of parts: {len(parts)}")
            
            for part in parts:
                question_sets = part.get('question_sets', [])
                total_questions_in_part = sum(len(qs.get('questions', [])) for qs in question_sets)
                logger.info(f"  - Part '{part.get('title')}': {len(question_sets)} question sets, {total_questions_in_part} questions")
                
                for qs in question_sets:
                    logger.info(f"    - {qs.get('type')}: {len(qs.get('questions', []))} questions, {len(qs.get('options', []))} options")
        
        # In errors nếu có
        if result['errors']:
            logger.error("Errors encountered:")
            for error in result['errors']:
                logger.error(f"  - {error}")
        
        # In warnings nếu có
        if result['warnings']:
            logger.warning("Warnings:")
            for warning in result['warnings']:
                logger.warning(f"  - {warning}")
        
        return result
        
    except FileNotFoundError:
        logger.error(f"Input file not found: {input_file}")
        return None
    except Exception as e:
        logger.error(f"Error during migration: {str(e)}")
        raise

def main():
    """Main function"""
    logger.info("Starting AI Migration Test")
    
    # Check command line arguments for mock mode
    import sys
    use_mock_llm = "--mock" in sys.argv
    
    if use_mock_llm:
        logger.info("🚀 Running in MOCK mode for fast testing")
    
    try:
        result = asyncio.run(test_ai_migration(use_mock_llm=use_mock_llm))
        
        if result:
            if result['status'] == 'COMPLETED' or str(result['status']) == 'MigrationStatus.COMPLETED':
                logger.info("✅ AI Migration test completed successfully!")
            else:
                logger.error(f"❌ AI Migration test failed with status: {result['status']}")
        else:
            logger.error("❌ AI Migration test failed - no result returned")
            
    except Exception as e:
        logger.error(f"❌ AI Migration test failed with exception: {str(e)}")
        raise

if __name__ == "__main__":
    main() 