from typing import Annotated
from fastmcp import FastMCP
from fastmcp.server.auth.providers.bearer import BearerAuthProvider, RSAKeyPair
from mcp import ErrorData, McpError
from mcp.server.auth.provider import AccessToken
from mcp.types import INTERNAL_ERROR
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN", "<generated_token>")  # Replace with your application key
MY_NUMBER = os.getenv("MY_NUMBER", "9189XXXXXXXX")  # Replace with your phone number

class RichToolDescription(BaseModel):
    description: str
    use_when: str
    side_effects: str | None


class SimpleBearerAuthProvider(BearerAuthProvider):
    """
    A simple BearerAuthProvider that does not require any specific configuration.
    It allows any valid bearer token to access the MCP server.
    """

    def __init__(self, token: str):
        k = RSAKeyPair.generate()
        super().__init__(
            public_key=k.public_key, jwks_uri=None, issuer=None, audience=None
        )
        self.token = token

    async def load_access_token(self, token: str) -> AccessToken | None:
        if token == self.token:
            return AccessToken(
                token=token,
                client_id="unknown",
                scopes=[],
                expires_at=None,  # No expiration for simplicity
            )
        return None


mcp = FastMCP(
    "My MCP Server",
    auth=SimpleBearerAuthProvider(TOKEN),
)

# Register core tools (resume and validate)
def register_core_tools(mcp):
    """Register core tools (resume, validate) with the MCP server."""
    
    ResumeToolDescription = RichToolDescription(
        description="Serve your resume in plain markdown.",
        use_when="Puch (or anyone) asks for your resume; this must return raw markdown, no extra formatting.",
        side_effects=None,
    )

    @mcp.tool(description=ResumeToolDescription.model_dump_json())
    async def resume() -> str:
        """
        Return your resume exactly as markdown text.
        
        This function reads the resume.md file from the current directory
        and returns its content as markdown text.
        
        Returns:
            str: The resume content in markdown format
            
        Raises:
            McpError: If the resume file cannot be found or read
        """
        try:
            resume_path = Path(__file__).parent / "resume.md"
            if not resume_path.exists():
                raise McpError(
                    ErrorData(
                        code=INTERNAL_ERROR,
                        message="Resume file not found. Please create resume.md"
                    )
                )
            
            resume_content = resume_path.read_text(encoding='utf-8')
            if not resume_content.strip():
                raise McpError(
                    ErrorData(
                        code=INTERNAL_ERROR,
                        message="Resume file is empty"
                    )
                )
            print(f"Serving resume from {resume_path}\n")
            print(f"Resume content:\n{resume_content}\n") 
            return resume_content
            
        except Exception as e:
            if isinstance(e, McpError):
                raise
            raise McpError(
                ErrorData(
                    code=INTERNAL_ERROR,
                    message=f"Error reading resume: {str(e)}"
                )
            )

    @mcp.tool
    async def validate() -> str:
        """
        NOTE: This tool must be present in an MCP server used by puch.
        """
        return MY_NUMBER

# Register the core tools
register_core_tools(mcp)


async def main():
    print(f" Starting MCP Server...")
    print(f" Server URL: http://localhost:8086/mcp")
  #  print(f"📄 Resume file: {Path(__file__).parent / 'resume.md'}")
    print("-" * 50)
    await mcp.run_async(
        "streamable-http",
        host="localhost",
        port=8085,
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main()) 