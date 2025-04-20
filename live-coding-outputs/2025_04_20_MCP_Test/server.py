from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv(".env")

# Create an MCP server
mcp = FastMCP(
    name="Calculator",
    host="0.0.0.0",  # only used for SSE transport (localhost)
    port=8050,       # only used for SSE transport (set this to any port)
)

# Add a simple calculator tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

# --- In server.py ---
if __name__ == "__main__":
    # Choose transport - hardcoded for this example
    transport_mode = "stdio"

    print(f"Attempting to run server with {transport_mode} transport") # Use f-string

    if transport_mode == "stdio":
        mcp.run(transport="stdio")
    elif transport_mode == "sse":
        # Ensure host/port are correctly configured if using SSE
        print(f"Running on http://{mcp.host}:{mcp.port}")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport mode: {transport_mode}")