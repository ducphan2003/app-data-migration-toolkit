#!/usr/bin/env python3
"""
Test script để validate logic parallel migration
"""

import json
import logging
from typing import Dict, Any

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def simulate_migration_result(part_index: int, has_valid_data: bool = True) -> Dict[str, Any]:
    """
    Simulate migration result cho test
    """
    if has_valid_data:
        return {
            'parts': [{
                'id': f'part_{part_index}',
                'title': f'Part {part_index}',
                'sort': part_index,
                'order': part_index
            }],
            'question_sets': [
                {
                    'id': f'qset_{part_index}_1',
                    'part_id': f'part_{part_index}',
                    'title': f'Question Set {part_index}.1'
                },
                {
                    'id': f'qset_{part_index}_2',
                    'part_id': f'part_{part_index}',
                    'title': f'Question Set {part_index}.2'
                }
            ],
            'questions': [
                {
                    'id': f'q_{part_index}_1_1',
                    'question_set_id': f'qset_{part_index}_1',
                    'title': f'Question {part_index}.1.1'
                },
                {
                    'id': f'q_{part_index}_1_2',
                    'question_set_id': f'qset_{part_index}_1',
                    'title': f'Question {part_index}.1.2'
                },
                {
                    'id': f'q_{part_index}_2_1',
                    'question_set_id': f'qset_{part_index}_2',
                    'title': f'Question {part_index}.2.1'
                }
            ]
        }
    else:
        # Simulate empty/invalid result
        return {
            'parts': [{
                'id': f'part_{part_index}',
                'title': f'Part {part_index}',
                'sort': part_index,
                'order': part_index
            }],
            'question_sets': [],
            'questions': []
        }

def test_merge_logic():
    """
    Test merge logic với different scenarios
    """
    logger.info("🧪 Testing merge logic...")
    
    # Scenario 1: Tất cả parts đều hợp lệ
    logger.info("\n📝 Scenario 1: All parts valid")
    parts_collection = []
    for i in range(1, 4):
        result = simulate_migration_result(i, has_valid_data=True)
        parts_collection.append({
            'part_index': i,
            'part': result['parts'][0],
            'question_sets': result['question_sets'],
            'questions': result['questions']
        })
    
    final_parts, final_question_sets, final_questions = filter_and_merge_parts(parts_collection)
    logger.info(f"Result: {len(final_parts)} parts, {len(final_question_sets)} question_sets, {len(final_questions)} questions")
    
    # Scenario 2: Part 2 bị rỗng
    logger.info("\n📝 Scenario 2: Part 2 empty")
    parts_collection = []
    for i in range(1, 4):
        has_data = i != 2  # Part 2 sẽ rỗng
        result = simulate_migration_result(i, has_valid_data=has_data)
        parts_collection.append({
            'part_index': i,
            'part': result['parts'][0],
            'question_sets': result['question_sets'],
            'questions': result['questions']
        })
    
    final_parts, final_question_sets, final_questions = filter_and_merge_parts(parts_collection)
    logger.info(f"Result: {len(final_parts)} parts, {len(final_question_sets)} question_sets, {len(final_questions)} questions")
    
    # Scenario 3: Duplicate parts (simulate bug)
    logger.info("\n📝 Scenario 3: Duplicate parts")
    parts_collection = []
    for i in range(1, 4):
        result = simulate_migration_result(i, has_valid_data=True)
        parts_collection.append({
            'part_index': i,
            'part': result['parts'][0],
            'question_sets': result['question_sets'],
            'questions': result['questions']
        })
    
    # Add duplicates
    for i in range(1, 4):
        result = simulate_migration_result(i, has_valid_data=False)  # Duplicates are empty
        parts_collection.append({
            'part_index': i + 3,
            'part': result['parts'][0],
            'question_sets': result['question_sets'],
            'questions': result['questions']
        })
    
    final_parts, final_question_sets, final_questions = filter_and_merge_parts(parts_collection)
    logger.info(f"Result: {len(final_parts)} parts, {len(final_question_sets)} question_sets, {len(final_questions)} questions")

def filter_and_merge_parts(parts_collection):
    """
    Apply same logic as in ParallelMigrateService._merge_parts_background
    """
    final_parts = []
    final_question_sets = []
    final_questions = []
    
    for part_data in parts_collection:
        part = part_data['part']
        question_sets = part_data['question_sets']
        questions = part_data['questions']
        part_index = part_data['part_index']
        
        # Kiểm tra part có hợp lệ không (có question_sets và questions)
        if part and question_sets and len(question_sets) > 0 and questions and len(questions) > 0:
            # Đảm bảo part có sort/order đúng
            if 'sort' not in part or part['sort'] is None:
                part['sort'] = part_index
            if 'order' not in part or part['order'] is None:
                part['order'] = part_index
            
            final_parts.append(part)
            final_question_sets.extend(question_sets)
            final_questions.extend(questions)
            
            logger.info(f"✓ Added valid part {part_index} (sort: {part.get('sort')}) with {len(question_sets)} question sets and {len(questions)} questions")
        else:
            logger.warning(f"✗ Skipped part {part_index} - empty question_sets or questions. Part: {part is not None}, QSets: {len(question_sets) if question_sets else 0}, Questions: {len(questions) if questions else 0}")
    
    # Sắp xếp parts theo thứ tự
    final_parts.sort(key=lambda x: x.get('sort', 0))
    
    # Kiểm tra nếu có quá nhiều parts
    if len(final_parts) > 3:
        logger.warning(f"Found {len(final_parts)} parts, expected maximum 3. Keeping only first 3 by sort order.")
        final_parts = final_parts[:3]
        
        # Filter question_sets và questions tương ứng với 3 parts được giữ lại
        valid_part_ids = [p.get('id') for p in final_parts if p.get('id')]
        if valid_part_ids:
            original_qs_count = len(final_question_sets)
            original_q_count = len(final_questions)
            
            final_question_sets = [qs for qs in final_question_sets if qs.get('part_id') in valid_part_ids]
            final_questions = [q for q in final_questions if any(qs.get('id') == q.get('question_set_id') for qs in final_question_sets)]
            
            logger.info(f"Filtered question_sets: {original_qs_count} -> {len(final_question_sets)}")
            logger.info(f"Filtered questions: {original_q_count} -> {len(final_questions)}")
    
    # Re-index parts để đảm bảo thứ tự 1, 2, 3
    for i, part in enumerate(final_parts, 1):
        part['sort'] = i
        part['order'] = i
    
    return final_parts, final_question_sets, final_questions

if __name__ == "__main__":
    logger.info("Test parallel migration logic")
    test_merge_logic()
    logger.info("\n✅ Test completed!") 