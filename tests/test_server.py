#!/usr/bin/env python3
"""
Simple test script to verify MCP server functionality.
Run this after starting the server to test basic functionality.
"""

import asyncio
import httpx
from pathlib import Path

async def test_server():
    """Test the MCP server endpoints."""
    
    # Server configuration
    base_url = "http://localhost:8085"
    
    print("🧪 Testing MCP Server...")
    print(f"Server URL: {base_url}")
    print("-" * 50)
    
    async with httpx.AsyncClient() as client:
        try:
            # Test 1: Check if server is running
            print("1. Testing server availability...")
            response = await client.get(f"{base_url}/health", timeout=5)
            print(f"   ✅ Server is running (Status: {response.status_code})")
        except httpx.RequestError as e:
            print(f"   ❌ Server not accessible: {e}")
            print("   Make sure the server is running with: python main.py")
            return
        
        # Test 2: Check if resume.md exists
        print("\n2. Testing resume file...")
        resume_path = Path("../resume.md")
        if resume_path.exists():
            content = resume_path.read_text(encoding='utf-8')
            if content.strip():
                print(f"   ✅ Resume file exists and has content ({len(content)} characters)")
            else:
                print("   ⚠️  Resume file exists but is empty")
        else:
            print("   ❌ Resume file not found. Please create resume.md")
        
        # Test 3: Check environment variables
        print("\n3. Testing environment variables...")
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        token = os.getenv("TOKEN")
        my_number = os.getenv("MY_NUMBER")
        
        if token and token != "<generated_token>":
            print("   ✅ TOKEN is set")
        else:
            print("   ⚠️  TOKEN not set or using default value")
        
        if my_number and my_number != "9189XXXXXXXX":
            print("   ✅ MY_NUMBER is set")
        else:
            print("   ⚠️  MY_NUMBER not set or using default value")
        
        # Test 4: Test MCP endpoint (basic connectivity)
        print("\n4. Testing MCP endpoint...")
        try:
            response = await client.get(f"{base_url}/mcp", timeout=5)
            print(f"   ✅ MCP endpoint accessible (Status: {response.status_code})")
        except httpx.RequestError as e:
            print(f"   ❌ MCP endpoint not accessible: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Next Steps:")
    print("1. Update your .env file with your actual TOKEN and MY_NUMBER")
    print("2. Customize resume.md with your actual resume")
    print("3. Deploy to a publicly accessible server")
    print("4. Connect to Puch AI using: /mcp connect <YOUR_SERVER_URL>/mcp <YOUR_TOKEN>")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_server())
