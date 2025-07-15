#!/usr/bin/env python3
"""
ESG Recommender Setup Script
Helps set up the development environment
"""

import os
import subprocess
import sys

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    env_file = os.path.join('backend', '.env')
    template_file = os.path.join('backend', '.env.template')
    
    if not os.path.exists(env_file) and os.path.exists(template_file):
        print("📝 Creating .env file from template...")
        with open(template_file, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Created .env file. You can edit it to add your Gemini API key.")
        return True
    elif os.path.exists(env_file):
        print("✅ .env file already exists")
        return True
    else:
        print("⚠️  .env template not found")
        return False

def install_backend_deps():
    """Install backend dependencies"""
    print("🐍 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'backend/requirements.txt'], 
                      check=True, cwd='.')
        print("✅ Backend dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install backend dependencies")
        return False

def install_frontend_deps():
    """Install frontend dependencies"""
    print("📦 Installing Node.js dependencies...")
    try:
        subprocess.run(['npm', 'install'], check=True, cwd='frontend')
        print("✅ Frontend dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install frontend dependencies")
        print("💡 Make sure Node.js and npm are installed")
        return False

def test_setup():
    """Test if setup is working"""
    print("🧪 Testing setup...")
    try:
        subprocess.run([sys.executable, 'test_setup.py'], check=True)
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Some tests failed, but this might be expected if servers aren't running")
        return False

def main():
    print("🌱 ESG Recommender Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('backend') or not os.path.exists('frontend'):
        print("❌ Please run this script from the ESG recommender root directory")
        sys.exit(1)
    
    success = True
    
    # Create .env file
    if not create_env_file():
        success = False
    
    # Install dependencies
    if not install_backend_deps():
        success = False
    
    if not install_frontend_deps():
        success = False
    
    print("\n" + "=" * 40)
    
    if success:
        print("🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Edit backend/.env to add your Gemini API key (optional)")
        print("2. Start backend: python backend/app.py")
        print("3. Start frontend: cd frontend && npm start")
        print("4. Visit http://localhost:3000")
    else:
        print("⚠️  Setup completed with some issues")
        print("💡 Check the error messages above and try manual installation")
    
    print("\n🔧 Quick start commands:")
    print("Windows: start_backend.bat & start_frontend.bat")
    print("Linux/Mac: ./start_backend.sh & ./start_frontend.sh")

if __name__ == '__main__':
    main()
