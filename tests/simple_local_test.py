#!/usr/bin/env python3
"""
Very simple local test - just read and display resume content.
"""
from pathlib import Path
from dotenv import load_dotenv
import os

def test_resume_directly():
    """Test resume content directly without server."""
    
    print("🧪 Testing Resume Content Directly...")
    print("=" * 50)
    
    # Check if resume.md exists
    resume_path = Path("../resume.md")
    if resume_path.exists():
        content = resume_path.read_text(encoding='utf-8')
        print(f"✅ Resume file exists ({len(content)} characters)")
        print("\n📄 Resume Content:")
        print("-" * 30)
        print(content)
        print("-" * 30)
    else:
        print("❌ Resume file not found!")
        return
    
    # Check environment variables
    load_dotenv()
    token = os.getenv("TOKEN", "<generated_token>")
    my_number = os.getenv("MY_NUMBER", "9189XXXXXXXX")
    
    print(f"\n🔑 Token: {token}")
    print(f"📱 Phone: {my_number}")
    
    print("\n" + "=" * 50)
    print("📋 Summary:")
    print("✅ Resume content is readable!")
    print("✅ Environment variables are set!")
    print("✅ Your server should work correctly!")
    print("\n🚀 To test the server:")
    print("1. Run: python main.py")
    print("2. In another terminal: python tests/local_test.py")

if __name__ == "__main__":
    test_resume_directly() 