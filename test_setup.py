#!/usr/bin/env python3
"""
Quick test script to verify the ESG Recommender setup
"""
import subprocess
import sys
import os

def test_backend():
    """Test backend dependencies and basic functionality"""
    print("🧪 Testing Backend...")
    
    # Check if we can import Flask app
    try:
        sys.path.append('api')
        from app import app
        print("✅ Flask app imports successfully")
    except ImportError as e:
        print(f"❌ Flask app import failed: {e}")
        return False
    
    # Test basic routes
    with app.test_client() as client:
        # Test health endpoint
        response = client.get('/api/health')
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
            
        # Test products endpoint
        response = client.get('/api/products')
        if response.status_code == 200:
            print("✅ Products endpoint working")
        else:
            print(f"❌ Products endpoint failed: {response.status_code}")
            return False
    
    return True

def test_frontend():
    """Test frontend dependencies"""
    print("🧪 Testing Frontend...")
    
    # Check if package.json exists
    if os.path.exists('frontend/package.json'):
        print("✅ Frontend package.json found")
    else:
        print("❌ Frontend package.json not found")
        return False
    
    # Check if src/App.js exists
    if os.path.exists('frontend/src/App.js'):
        print("✅ Frontend App.js found")
    else:
        print("❌ Frontend App.js not found")
        return False
    
    return True

def test_configuration():
    """Test deployment configuration"""
    print("🧪 Testing Configuration...")
    
    # Check required files
    required_files = [
        'Procfile',
        'requirements.txt',
        'render.yaml',
        'build.sh',
        '.env.template'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} not found")
            return False
    
    return True

if __name__ == "__main__":
    print("🚀 ESG Recommender Setup Test")
    print("=" * 40)
    
    # Change to project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run tests
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    config_ok = test_configuration()
    
    print("\n" + "=" * 40)
    
    if backend_ok and frontend_ok and config_ok:
        print("🎉 All tests passed! Ready for deployment.")
        print("\nNext steps:")
        print("1. Push to GitHub")
        print("2. Deploy on Render.com")
        print("3. Set environment variables")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
