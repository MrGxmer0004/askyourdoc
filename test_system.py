"""
Test script for AskYourDoc system
"""

import json
import requests
import base64
from pathlib import Path

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_BIOMARKERS = {
    "glucose": 110.0,
    "hba1c": 5.8,
    "total_cholesterol": 220.0,
    "ldl": 140.0,
    "hdl": 45.0,
    "tsh": 6.2,
    "crp": 2.5,
    "vitamin_d": 18.0
}

def test_knowledge_base_status():
    """Test knowledge base status endpoint"""
    print("🔍 Testing Knowledge Base Status...")
    try:
        response = requests.get(f"{BASE_URL}/knowledge-base/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Knowledge Base Status: {data}")
            return True
        else:
            print(f"❌ Knowledge Base Status failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Knowledge Base Status error: {e}")
        return False

def test_reference_ranges():
    """Test reference ranges endpoint"""
    print("\n📋 Testing Reference Ranges...")
    try:
        response = requests.get(f"{BASE_URL}/reference-ranges")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Reference Ranges loaded: {len(data['reference_ranges'])} ranges")
            print(f"✅ Abnormality Mappings: {len(data['abnormalities_mapping'])} mappings")
            return True
        else:
            print(f"❌ Reference Ranges failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Reference Ranges error: {e}")
        return False

def test_biomarker_analysis():
    """Test biomarker analysis endpoint"""
    print("\n🧪 Testing Biomarker Analysis...")
    try:
        payload = {
            "biomarker_data": TEST_BIOMARKERS,
            "user_symptoms": "I've been feeling tired and gaining weight recently. I also have some joint pain.",
            "user_lifestyle": "I work a desk job and don't exercise much. I eat mostly processed foods."
        }
        
        response = requests.post(f"{BASE_URL}/analyze/biomarkers", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✅ Biomarker Analysis successful!")
                print(f"📊 Analysis includes {len(data['analysis'])} main sections")
                
                # Print key insights
                analysis = data['analysis']
                print("\n📈 Key Insights:")
                print(f"- Overall Risk Level: {analysis['pillar_3_predictive_insights']['overall_risk_level']}")
                print(f"- Medical Consultation Required: {analysis['pillar_4_actionable_recommendations']['medical_consultation_required']}")
                print(f"- Number of Risk Assessments: {len(analysis['pillar_3_predictive_insights']['risk_assessments'])}")
                
                return True
            else:
                print(f"❌ Biomarker Analysis failed: {data['error']}")
                return False
        else:
            print(f"❌ Biomarker Analysis failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Biomarker Analysis error: {e}")
        return False

def test_knowledge_search():
    """Test knowledge base search"""
    print("\n🔍 Testing Knowledge Base Search...")
    try:
        queries = [
            "TSH hypothyroidism",
            "glucose diabetes risk",
            "cholesterol cardiovascular disease"
        ]
        
        for query in queries:
            response = requests.post(f"{BASE_URL}/search-knowledge", params={"query": query, "top_k": 3})
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Search '{query}': {len(data['results'])} results")
            else:
                print(f"❌ Search '{query}' failed: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Knowledge Search error: {e}")
        return False

def test_datasets():
    """Test datasets endpoint"""
    print("\n📊 Testing Datasets...")
    try:
        response = requests.get(f"{BASE_URL}/datasets")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Datasets loaded: {data['total_datasets']} datasets")
            for name, info in data['datasets'].items():
                print(f"  - {name}: {info['rows']} rows, {len(info['columns'])} columns")
            return True
        else:
            print(f"❌ Datasets failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Datasets error: {e}")
        return False

def test_health_check():
    """Test health check endpoint"""
    print("\n🏥 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']}")
            return True
        else:
            print(f"❌ Health Check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health Check error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting AskYourDoc System Tests\n")
    
    tests = [
        ("Health Check", test_health_check),
        ("Knowledge Base Status", test_knowledge_base_status),
        ("Reference Ranges", test_reference_ranges),
        ("Datasets", test_datasets),
        ("Knowledge Search", test_knowledge_search),
        ("Biomarker Analysis", test_biomarker_analysis),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")
    
    return passed == total

if __name__ == "__main__":
    print("AskYourDoc System Test Suite")
    print("Make sure the server is running on http://localhost:8000")
    print("Run: python main.py")
    print()
    
    input("Press Enter to start tests...")
    run_all_tests()
