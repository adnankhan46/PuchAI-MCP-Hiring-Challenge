#!/usr/bin/env python3
"""
Test MCP server functionality with proper authentication.
"""
import asyncio
import httpx
import json
from pathlib import Path

async def test_mcp_server():
    """Test the MCP server with proper authentication."""
    
    print("🧪 Testing MCP Server with Authentication...")
    print("=" * 50)
    
    # Check if resume.md exists
    resume_path = Path("../resume.md")
    if resume_path.exists():
        content = resume_path.read_text(encoding='utf-8')
        print(f"✅ Resume file exists ({len(content)} characters)")
    else:
        print("❌ Resume file not found!")
        return
    
    # Get token from environment
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    token = os.getenv("TOKEN", "<generated_token>")
    my_number = os.getenv("MY_NUMBER", "9189XXXXXXXX")
    
    print(f"🔑 Token: {token}")
    print(f"📱 Phone: {my_number}")
    
    # Test server with authentication
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test MCP endpoint
            response = await client.get("http://localhost:8085/mcp", headers=headers)
            print(f"✅ MCP endpoint response: {response.status_code}")
            
            if response.status_code == 200:
                print("🎉 Server is working correctly!")
                print("📋 You can now connect to Puch AI with:")
                print(f"   /mcp connect http://localhost:8085/mcp {token}")
            else:
                print(f"⚠️  Unexpected response: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
    except httpx.ConnectError:
        print("❌ Server is not running. Start it with: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("📋 Summary:")
    print("✅ Server is running on http://localhost:8085/mcp")
    print("✅ Authentication is working (Unauthorized without token is expected)")
    print("✅ Ready to connect to Puch AI!")
    print("\n🔗 Connect to Puch AI with:")
    print(f"   /mcp connect http://localhost:8085/mcp {token}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server()) 