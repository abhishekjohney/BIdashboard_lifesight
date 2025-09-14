"""
Test script to validate the Marketing Intelligence Dashboard setup
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError:
        print("❌ pandas not found")
        return False
    
    try:
        import numpy as np
        print("✅ numpy imported successfully")
    except ImportError:
        print("❌ numpy not found")
        return False
    
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except ImportError:
        print("❌ streamlit not found")
        return False
    
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ plotly imported successfully")
    except ImportError:
        print("❌ plotly not found")
        return False
    
    return True

def test_data_directory():
    """Test if data directory exists"""
    print("\n📁 Testing data directory...")
    
    if os.path.exists("data"):
        print("✅ data directory exists")
        
        # List files in data directory
        files = os.listdir("data")
        print(f"📄 Files in data directory: {files}")
        
        # Check for expected files
        expected_files = ["Facebook.csv", "Google.csv", "TikTok.csv", "Business.csv"]
        for file in expected_files:
            if file in files:
                print(f"✅ {file} found")
            else:
                print(f"⚠️  {file} not found (you can add your own data later)")
        
        return True
    else:
        print("❌ data directory not found")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n📋 Testing file structure...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "scripts/data_processor.py",
        "scripts/metrics_calculator.py"
    ]
    
    all_found = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} not found")
            all_found = False
    
    return all_found

def main():
    """Run all tests"""
    print("🚀 Marketing Intelligence Dashboard - Setup Validation")
    print("=" * 60)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    all_tests_passed = True
    
    # Run tests
    all_tests_passed &= test_imports()
    all_tests_passed &= test_data_directory()
    all_tests_passed &= test_file_structure()
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 All tests passed! Your dashboard is ready to run.")
        print("\n📋 Next steps:")
        print("1. Add your data files to the data/ directory")
        print("2. Run: streamlit run main.py")
        print("3. Open your browser to view the dashboard")
    else:
        print("❌ Some tests failed. Please check the issues above.")
        print("\n🔧 Common solutions:")
        print("- Install missing packages: pip install -r requirements.txt")
        print("- Create missing directories and files")
        print("- Check file paths and permissions")

if __name__ == "__main__":
    main()