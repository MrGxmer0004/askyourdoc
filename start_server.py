"""
Startup script for AskYourDoc server
"""

import uvicorn
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'pandas', 'numpy', 'scikit-learn',
        'sentence_transformers', 'faiss-cpu', 'PyPDF2', 'pytesseract'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstall missing packages with:")
        print("  pip install -r requirements.txt")
        return False
    
    return True

def check_data_files():
    """Check if required data files exist"""
    required_files = [
        'comprehensive_biomarkers_dataset.csv',
        'diabetes_prediabetes_dataset.csv',
        'thyroid_hypothyroid_dataset.csv',
        'dyslipidemia_cvd_dataset.csv',
        'inflammation_dataset.csv',
        'medical_labs_training_weaklabels.csv',
        'data.txt',
        'data (1).txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required data files:")
        for file in missing_files:
            print(f"  - {file}")
        print("\nMake sure all CSV and TXT files are in the current directory")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🚀 Starting AskYourDoc Server")
    print("=" * 40)
    
    # Check dependencies
    print("📦 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ All dependencies installed")
    
    # Check data files
    print("📊 Checking data files...")
    if not check_data_files():
        sys.exit(1)
    print("✅ All data files found")
    
    # Start server
    print("\n🌐 Starting server...")
    print("Server will be available at: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print("-" * 40)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
