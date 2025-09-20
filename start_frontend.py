"""
Frontend startup script for AskYourDoc
Automatically installs dependencies and starts the development server
"""

import subprocess
import sys
import os
from pathlib import Path

def check_node_installed():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False

def check_npm_installed():
    """Check if npm is installed"""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False

def install_dependencies():
    """Install npm dependencies"""
    print("📦 Installing dependencies...")
    try:
        result = subprocess.run(['npm', 'install'], check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print(f"Error output: {e.stderr}")
        return False

def start_dev_server():
    """Start the development server"""
    print("🚀 Starting development server...")
    print("Frontend will be available at: http://localhost:3000")
    print("Make sure the backend is running on http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run(['npm', 'run', 'dev'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start development server: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Development server stopped by user")
        return True

def main():
    """Main startup function"""
    print("🚀 Starting AskYourDoc Frontend")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path('package.json').exists():
        print("❌ package.json not found. Make sure you're in the frontend directory.")
        sys.exit(1)
    
    # Check Node.js and npm
    print("🔍 Checking prerequisites...")
    if not check_node_installed():
        print("Please install Node.js from https://nodejs.org/")
        sys.exit(1)
    
    if not check_npm_installed():
        print("Please install npm (usually comes with Node.js)")
        sys.exit(1)
    
    # Install dependencies if node_modules doesn't exist
    if not Path('node_modules').exists():
        if not install_dependencies():
            sys.exit(1)
    else:
        print("✅ Dependencies already installed")
    
    # Start development server
    start_dev_server()

if __name__ == "__main__":
    main()
