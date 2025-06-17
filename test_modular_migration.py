#!/usr/bin/env python3
"""
Test script cho modular migration workflow theo từng question type
"""
import asyncio
import json
import logging
from datetime import datetime

from app.services.ai_migration_agents import AIMigrationAgents

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_modular_migration():
    """Test migration workflow với logic modular theo từng question type"""
    
    print("🚀 Starting Modular Migration Test...")
    
    # Load test data
    try:
        with open('import-data-tool/raw-data/reading.input-fill_blank.json', 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        print(f"✅ Loaded test data with {len(test_data.get('parts', []))} parts")
    except FileNotFoundError:
        print("❌ Test data file not found")
        return
    
    # Initialize AI agents (sử dụng fallback mode)
    agents = AIMigrationAgents()
    print("✅ Initialized AI migration agents")
    
    # Test với part đầu tiên
    if test_data.get('parts'):
        part_data = test_data['parts'][0]
        print(f"📝 Testing with part: {part_data.get('title', 'Unknown')}")
        print(f"📊 Part has {len(part_data.get('questions', []))} questions")
        
        # Step 1: Analyze question types
        questions = part_data.get('questions', [])
        print("\n🔍 Step 1: Analyzing question types...")
        
        try:
            question_analyses = await agents.analyze_question_types(questions)
            print(f"✅ Analyzed {len(question_analyses)} questions")
            
            # Show detected types
            type_counts = {}
            for analysis in question_analyses:
                question_type = analysis.detected_type
                type_counts[question_type] = type_counts.get(question_type, 0) + 1
            
            print("📊 Detected question types:")
            for qtype, count in type_counts.items():
                print(f"   - {qtype}: {count} questions")
            
        except Exception as e:
            logger.error(f"Error in question analysis: {e}")
            # Fallback analysis
            question_analyses = agents._fallback_question_analysis(questions)
            print(f"⚠️  Used fallback analysis for {len(question_analyses)} questions")
        
        # Step 2: Transform using modular approach
        print("\n🔄 Step 2: Transforming with modular migration...")
        
        try:
            # Prepare full part data with quiz info
            full_part_data = {
                **test_data,  # Include quiz-level fields
                **part_data   # Include part-specific fields
            }
            
            migration_result = await agents.transform_to_question_sets_by_type(
                full_part_data, 
                question_analyses
            )
            
            print("✅ Migration completed successfully!")
            print(f"📊 Result summary:")
            print(f"   - Quiz data: {bool(migration_result.get('quiz'))}")
            print(f"   - Parts: {len(migration_result.get('parts', []))}")
            
            # Count nested question_sets and questions
            total_question_sets = 0
            total_questions = 0
            for part in migration_result.get('parts', []):
                part_question_sets = part.get('question_sets', [])
                total_question_sets += len(part_question_sets)
                for qs in part_question_sets:
                    total_questions += len(qs.get('questions', []))
            
            print(f"   - Question sets: {total_question_sets}")
            print(f"   - Questions: {total_questions}")
            
            # Show question sets by type (nested structure)
            if migration_result.get('parts'):
                print("\n📋 Question sets created:")
                for part_idx, part in enumerate(migration_result.get('parts', []), 1):
                    print(f"  Part {part_idx}: {part.get('title', 'Unknown')}")
                    for qs in part.get('question_sets', []):
                        print(f"   - {qs.get('question_type')}: {qs.get('title')} ({qs.get('question_count')} questions)")
            
            # Save result for inspection
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"import-data-tool/test-result/modular_migration_result_{timestamp}.json"
            
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(migration_result, f, ensure_ascii=False, indent=2)
                print(f"💾 Saved result to: {output_file}")
            except Exception as e:
                logger.error(f"Error saving result: {e}")
            
            # Show sample question set (nested structure)
            if migration_result.get('parts') and migration_result['parts'][0].get('question_sets'):
                sample_qs = migration_result['parts'][0]['question_sets'][0]
                print(f"\n📄 Sample question set ({sample_qs.get('question_type')}):")
                print(f"   Title: {sample_qs.get('title')}")
                print(f"   Description: {sample_qs.get('description', '')[:100]}...")
                print(f"   Question count: {sample_qs.get('question_count')}")
                print(f"   Content preview: {sample_qs.get('content', '')[:150]}...")
                
                # Show sample question (nested structure)
                if sample_qs.get('questions'):
                    sample_q = sample_qs['questions'][0]
                    print(f"\n❓ Sample question:")
                    print(f"   Order: {sample_q.get('order')}")
                    print(f"   Type: {sample_q.get('question_type')}")
                    print(f"   Correct answers: {sample_q.get('correct_answers')}")
                    print(f"   Explanation: {sample_q.get('explain', '')[:100]}...")
            
        except Exception as e:
            logger.error(f"Error in modular migration: {e}")
            print("❌ Migration failed")
    
    else:
        print("❌ No parts found in test data")

def test_question_type_detection():
    """Test question type detection logic"""
    print("\n🧪 Testing question type detection...")
    
    # Load test data
    try:
        with open('import-data-tool/raw-data/reading.input-fill_blank.json', 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        agents = AIMigrationAgents()
        
        if test_data.get('parts'):
            questions = test_data['parts'][0].get('questions', [])
            
            print(f"📊 Testing {len(questions)} questions:")
            for i, question in enumerate(questions[:3]):  # Test first 3 questions
                detected_type = agents._simple_type_detection(question)
                print(f"   Question {i+1}:")
                print(f"     - Type field: {question.get('type')}")
                print(f"     - Question type: {question.get('question_type')}")
                print(f"     - Detected: {detected_type}")
                print(f"     - Has gap_fill_in_blank: {bool(question.get('gap_fill_in_blank'))}")
                print(f"     - Has single_choice_radio: {bool(question.get('single_choice_radio'))}")
                print(f"     - Has selection: {bool(question.get('selection'))}")
                print(f"     - Has mutilple_choice: {bool(question.get('mutilple_choice'))}")
                print()
                
    except Exception as e:
        logger.error(f"Error in question type detection test: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 MODULAR MIGRATION TEST")
    print("=" * 60)
    
    # Run tests
    asyncio.run(test_modular_migration())
    test_question_type_detection()
    
    print("\n" + "=" * 60)
    print("✅ Test completed!")
    print("=" * 60) 