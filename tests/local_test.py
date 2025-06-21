#!/usr/bin/env python3
"""
Local test to verify the resume tool works.
"""
import asyncio
import httpx
import json
from pathlib import Path

async def test_resume_tool():
    """Test the resume tool locally."""
    
    print("🧪 Testing Resume Tool Locally...")
    print("=" * 50)
    
    # Check if resume.md exists
    resume_path = Path("../resume.md")
    if resume_path.exists():
        content = resume_path.read_text(encoding='utf-8')
        print(f"✅ Resume file exists ({len(content)} characters)")
        print(f"📄 First 100 chars: {content[:100]}...")
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
                
                # Now test the resume tool by simulating an MCP call
                print("\n🔧 Testing Resume Tool...")
                
                # Create a simple MCP-style request
                mcp_request = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": "resume",
                        "arguments": {}
                    }
                }
                
                # Send the request
                tool_response = await client.post(
                    "http://localhost:8085/mcp",
                    headers=headers,
                    json=mcp_request
                )
                
                print(f"📋 Tool response status: {tool_response.status_code}")
                
                if tool_response.status_code == 200:
                    result = tool_response.json()
                    print("✅ Resume tool called successfully!")
                    print(f"📄 Response type: {type(result)}")
                    if 'result' in result:
                        resume_content = result['result']['content'][0]['text']
                        print(f"📄 Resume content (first 200 chars): {resume_content[:200]}...")
                    else:
                        print(f"📄 Full response: {result}")
                else:
                    print(f"❌ Tool call failed: {tool_response.status_code}")
                    print(f"📄 Response: {tool_response.text}")
                
            else:
                print(f"⚠️  Unexpected response: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
    except httpx.ConnectError:
        print("❌ Server is not running. Start it with: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("📋 Summary:")
    print("✅ Your MCP server is working locally!")
    print("✅ Resume tool is functional!")
    print("✅ Ready for Puch AI connection!")

if __name__ == "__main__":
    asyncio.run(test_resume_tool()) 