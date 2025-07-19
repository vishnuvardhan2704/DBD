#!/usr/bin/env python3
"""
Pre-deployment verification script for Render.com
"""
import os
import sys
import subprocess

def check_file_exists(filepath):
    """Check if a file exists and print result"""
    if os.path.exists(filepath):
        print(f"✅ {filepath}")
        return True
    else:
        print(f"❌ {filepath} - MISSING!")
        return False

def check_directory_structure():
    """Verify the project structure"""
    print("🔍 Checking Project Structure...")
    
    required_files = [
        "api/app.py",
        "api/db.py", 
        "api/requirements.txt",
        "frontend/package.json",
        "frontend/src/App.js",
        "build.sh",
        "Procfile",
        "render.yaml",
        "requirements.txt"
    ]
    
    all_good = True
    for file in required_files:
        if not check_file_exists(file):
            all_good = False
    
    return all_good

def check_build_script():
    """Check if build script is properly configured"""
    print("\n🔧 Checking Build Configuration...")
    
    if os.path.exists("build.sh"):
        with open("build.sh", "r") as f:
            content = f.read()
            
        if "npm install" in content and "npm run build" in content:
            print("✅ build.sh contains frontend build commands")
        else:
            print("❌ build.sh missing frontend build commands")
            return False
            
        if "cp -r frontend/build/* api/static/" in content:
            print("✅ build.sh copies frontend to static folder")
        else:
            print("❌ build.sh doesn't copy frontend build")
            return False
            
        return True
    else:
        print("❌ build.sh not found")
        return False

def check_flask_app():
    """Check Flask app configuration"""
    print("\n🐍 Checking Flask App...")
    
    try:
        # Change to api directory
        original_dir = os.getcwd()
        os.chdir("api")
        
        # Try to import the app
        import sys
        sys.path.append(".")
        from app import app
        
        print("✅ Flask app imports successfully")
        
        # Check if static folder is configured
        if hasattr(app, 'static_folder'):
            print("✅ Flask app configured for static files")
        else:
            print("❌ Flask app not configured for static files")
            return False
        
        # Test basic route
        with app.test_client() as client:
            response = client.get('/api/health')
            if response.status_code == 200:
                print("✅ Health endpoint working")
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                return False
        
        os.chdir(original_dir)
        return True
        
    except Exception as e:
        print(f"❌ Flask app error: {e}")
        os.chdir(original_dir)
        return False

def main():
    """Main verification function"""
    print("🚀 ESG Recommender - Render Deployment Verification")
    print("=" * 60)
    
    # Change to project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run checks
    structure_ok = check_directory_structure()
    build_ok = check_build_script()
    flask_ok = check_flask_app()
    
    print("\n" + "=" * 60)
    print("📊 VERIFICATION RESULTS:")
    print(f"  📁 Project Structure: {'✅ PASS' if structure_ok else '❌ FAIL'}")
    print(f"  🔧 Build Script: {'✅ PASS' if build_ok else '❌ FAIL'}")
    print(f"  🐍 Flask App: {'✅ PASS' if flask_ok else '❌ FAIL'}")
    
    if structure_ok and build_ok and flask_ok:
        print("\n🎉 ALL CHECKS PASSED!")
        print("\n🚀 Ready for Render deployment!")
        print("\nNext steps:")
        print("1. git add . && git commit -m 'Ready for Render'")
        print("2. git push origin main")
        print("3. Deploy on render.com")
        return 0
    else:
        print("\n❌ Some checks failed!")
        print("Please fix the issues above before deploying.")
        return 1

if __name__ == "__main__":
    exit(main())
