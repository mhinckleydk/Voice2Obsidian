#!/usr/bin/env python3
"""
Voice Journal Setup Script
This script sets up the voice journal environment with all dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description=""):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}")
    try:
        if platform.system() == "Windows":
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command.split(), check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_directories():
    """Create necessary directories"""
    print("📁 Creating necessary directories...")
    directories = [
        'sessions',
        'recordings_to_summarize',
        'obsidian/VoiceNotes'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ Created/verified: {directory}")
    
    return True

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python dependencies...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing requirements"):
        return False
    
    return True

def check_ollama():
    """Check if Ollama is available"""
    print("🤖 Checking Ollama availability...")
    try:
        import requests
        response = requests.get('http://localhost:11434/api/version', timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running and accessible")
            return True
        else:
            print("⚠️  Ollama server responded but with unexpected status")
            return False
    except Exception as e:
        print("⚠️  Ollama not accessible. Make sure Ollama is installed and running:")
        print("   1. Install Ollama from https://ollama.ai/")
        print("   2. Run: ollama serve")
        print("   3. Pull a model: ollama pull llama3")
        return False

def create_example_config():
    """Create an example configuration file"""
    print("⚙️  Checking configuration...")
    
    config_path = Path("config/settings.py")
    if config_path.exists():
        print("✅ Configuration file already exists")
        return True
    
    print("📝 Configuration file not found - it should already exist in your project")
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up Voice Journal Environment")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("❌ Failed to create directories")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    # Check configuration
    create_example_config()
    
    # Check Ollama (optional)
    check_ollama()
    
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("\nNext steps:")
    print("1. Make sure Ollama is running: ollama serve")
    print("2. Pull a model if needed: ollama pull llama3")
    print("3. Update config/settings.py with your preferred paths")
    print("4. Run the journal: python scripts/journal.py")
    print("5. Or process existing recordings: python scripts/preloaded_recording.py")
    print("\nFor help, check the README.md file.")

if __name__ == "__main__":
    main()
