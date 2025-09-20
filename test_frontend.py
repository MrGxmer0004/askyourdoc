"""
Frontend test script for AskYourDoc
Tests the React frontend functionality and integration
"""

import requests
import time
import subprocess
import sys
import os
from pathlib import Path

# Test configuration
FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8000"

def test_backend_connection():
    """Test if backend is running"""
    print("🔍 Testing Backend Connection...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend connection failed: {e}")
        print("Make sure the backend is running on http://localhost:8000")
        return False

def test_frontend_connection():
    """Test if frontend is running"""
    print("\n🌐 Testing Frontend Connection...")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running")
            return True
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend connection failed: {e}")
        print("Make sure the frontend is running on http://localhost:3000")
        return False

def test_backend_endpoints():
    """Test backend API endpoints"""
    print("\n🔌 Testing Backend Endpoints...")
    
    endpoints = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/knowledge-base/status", "Knowledge base status"),
        ("/reference-ranges", "Reference ranges"),
        ("/datasets", "Datasets")
    ]
    
    results = []
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {description}: OK")
                results.append(True)
            else:
                print(f"❌ {description}: Status {response.status_code}")
                results.append(False)
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: {e}")
            results.append(False)
    
    return all(results)

def test_file_upload_endpoint():
    """Test file upload endpoint with a sample request"""
    print("\n📁 Testing File Upload Endpoint...")
    
    # Create a simple test file
    test_content = b"Test PDF content"
    
    try:
        # Test with a simple text file (simulating PDF)
        files = {'file': ('test.txt', test_content, 'text/plain')}
        data = {'user_symptoms': 'Test symptoms for analysis'}
        
        response = requests.post(
            f"{BACKEND_URL}/analyze/lab-report",
            files=files,
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ File upload endpoint working")
                return True
            else:
                print(f"❌ File upload failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ File upload endpoint returned status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ File upload test failed: {e}")
        return False

def test_frontend_build():
    """Test if frontend can be built"""
    print("\n🏗️ Testing Frontend Build...")
    
    if not Path('package.json').exists():
        print("❌ package.json not found")
        return False
    
    try:
        # Check if node_modules exists
        if not Path('node_modules').exists():
            print("📦 Installing dependencies...")
            result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Failed to install dependencies: {result.stderr}")
                return False
        
        # Try to build the project
        print("🔨 Building frontend...")
        result = subprocess.run(['npm', 'run', 'build'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Frontend build successful")
            return True
        else:
            print(f"❌ Frontend build failed: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js and npm")
        return False
    except Exception as e:
        print(f"❌ Build test failed: {e}")
        return False

def test_cors_configuration():
    """Test CORS configuration between frontend and backend"""
    print("\n🌐 Testing CORS Configuration...")
    
    try:
        # Test preflight request
        headers = {
            'Origin': FRONTEND_URL,
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        response = requests.options(
            f"{BACKEND_URL}/analyze/lab-report",
            headers=headers,
            timeout=5
        )
        
        if response.status_code in [200, 204]:
            print("✅ CORS preflight request successful")
            return True
        else:
            print(f"❌ CORS preflight failed: Status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ CORS test failed: {e}")
        return False

def run_all_tests():
    """Run all frontend tests"""
    print("🧪 AskYourDoc Frontend Test Suite")
    print("=" * 50)
    
    tests = [
        ("Backend Connection", test_backend_connection),
        ("Frontend Connection", test_frontend_connection),
        ("Backend Endpoints", test_backend_endpoints),
        ("File Upload Endpoint", test_file_upload_endpoint),
        ("Frontend Build", test_frontend_build),
        ("CORS Configuration", test_cors_configuration),
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
        print("🎉 All tests passed! Frontend is ready for use.")
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")
    
    return passed == total

if __name__ == "__main__":
    print("AskYourDoc Frontend Test Suite")
    print("Make sure both frontend and backend servers are running:")
    print("  Frontend: http://localhost:3000")
    print("  Backend: http://localhost:8000")
    print()
    
    input("Press Enter to start tests...")
    run_all_tests()
