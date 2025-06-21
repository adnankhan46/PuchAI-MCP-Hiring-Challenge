#!/usr/bin/env python3
"""
Simple health check script for the MCP server.
This can be used to verify the server is running correctly.
"""

import asyncio
import httpx
import os
from pathlib import Path

async def health_check():
    """Check if the MCP server is healthy."""
    
    # Get server URL from environment or use default
    port = os.getenv("PORT", "8085")
    base_url = f"http://localhost:{port}"
    
    print(f"🏥 Health Check for MCP Server")
    print(f"Server URL: {base_url}")
    print("-" * 50)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # Test basic connectivity
            response = await client.get(f"{base_url}/mcp")
            print(f"✅ Server is responding (Status: {response.status_code})")
            
            # Check if resume file exists
            resume_path = Path("resume.md")
            if resume_path.exists():
                content = resume_path.read_text(encoding='utf-8')
                print(f"✅ Resume file exists ({len(content)} characters)")
            else:
                print("❌ Resume file not found")
                return False
            
            # Check environment variables
            token = os.getenv("TOKEN")
            my_number = os.getenv("MY_NUMBER")
            
            if token and token != "<generated_token>":
                print("✅ TOKEN is configured")
            else:
                print("⚠️  TOKEN not configured")
            
            if my_number and my_number != "9189XXXXXXXX":
                print("✅ MY_NUMBER is configured")
            else:
                print("⚠️  MY_NUMBER not configured")
            
            print("\n🎉 Health check passed!")
            return True
            
        except httpx.ConnectError:
            print("❌ Server is not running")
            return False
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False

if __name__ == "__main__":
    asyncio.run(health_check()) 