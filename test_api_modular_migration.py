#!/usr/bin/env python3
"""
Test script để kiểm tra API /migrate-data với logic modular migration
"""
import asyncio
import json
import requests
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API Configuration
API_BASE_URL = "http://localhost:8000"  # Adjust if needed
MIGRATE_ENDPOINT = f"{API_BASE_URL}/api/v1/migrate-data"

def test_api_migrate_data():
    """Test API /migrate-data với dữ liệu MULTIPLE_CHOICE_MANY"""
    
    print("🚀 Testing API /migrate-data with modular approach...")
    
    # Load test data
    try:
        with open('import-data-tool/raw-data/reading.input-multiple_choice_many.json', 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        print(f"✅ Loaded test data with {len(test_data.get('parts', []))} parts")
    except FileNotFoundError:
        print("❌ Test data file not found")
        return
    
    # Prepare request payload
    payload = {
        "id": test_data.get("id", 1714),
        "title": test_data.get("title", "Test Migration"),
        "parts": test_data.get("parts", [])
    }
    
    # Mock authentication header (adjust as needed)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer mock-jwt-token"  # Replace with actual token if needed
    }
    
    try:
        print("📡 Sending request to API...")
        response = requests.post(
            MIGRATE_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=300  # 5 minutes timeout
        )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API call successful!")
            print(f"📋 Migration process created:")
            print(f"   - Process ID: {result.get('id')}")
            print(f"   - Status: {result.get('status')}")
            print(f"   - Progress: {result.get('progress_percentage', 0)}%")
            print(f"   - Current step: {result.get('current_step')}")
            
            # Show processing logs if available
            if result.get('processing_logs'):
                print(f"\n📝 Processing logs ({len(result['processing_logs'])} entries):")
                for log in result['processing_logs'][-3:]:  # Show last 3 logs
                    print(f"   [{log.get('step')}] {log.get('message')}")
            
            # Show final result if completed
            if result.get('final_result'):
                final_result = result['final_result']
                quiz_data = final_result.get('quiz', {})
                parts_data = final_result.get('parts', [])
                
                print(f"\n🎯 Final result summary:")
                print(f"   - Quiz title: {quiz_data.get('title')}")
                print(f"   - Parts: {len(parts_data)}")
                
                # Count question sets and questions
                total_question_sets = 0
                total_questions = 0
                for part in parts_data:
                    part_question_sets = part.get('question_sets', [])
                    total_question_sets += len(part_question_sets)
                    for qs in part_question_sets:
                        total_questions += len(qs.get('questions', []))
                
                print(f"   - Question sets: {total_question_sets}")
                print(f"   - Questions: {total_questions}")
                
                # Show question sets by type
                if parts_data:
                    print(f"\n📋 Question sets created:")
                    for part_idx, part in enumerate(parts_data, 1):
                        print(f"  Part {part_idx}: {part.get('title', 'Unknown')}")
                        for qs in part.get('question_sets', []):
                            print(f"   - {qs.get('question_type')}: {qs.get('title')} ({qs.get('question_count')} questions)")
                
                # Save result for inspection
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"import-data-tool/test-result/api_migration_result_{timestamp}.json"
                
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(result, f, ensure_ascii=False, indent=2)
                    print(f"💾 Saved API result to: {output_file}")
                except Exception as e:
                    logger.error(f"Error saving result: {e}")
            
        else:
            print("❌ API call failed!")
            print(f"📄 Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - is the API server running?")
        print("💡 Try running: python app/main.py")
    except requests.exceptions.Timeout:
        print("⏰ Request timeout - migration may take longer")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_api_status():
    """Test API health status"""
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        if response.status_code == 200:
            print("✅ API server is running")
            return True
        else:
            print(f"⚠️  API server responded with: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        return False
    except Exception as e:
        print(f"❌ Error checking API status: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 API MODULAR MIGRATION TEST")
    print("=" * 60)
    
    # Check API status first
    print("🔍 Checking API server status...")
    if test_api_status():
        # Run migration test
        test_api_migrate_data()
    else:
        print("💡 Please start the API server first:")
        print("   python app/main.py")
    
    print("\n" + "=" * 60)
    print("✅ Test completed!")
    print("=" * 60) 