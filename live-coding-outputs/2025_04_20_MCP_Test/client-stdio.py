import sys
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main(a, b):
    # Since the server is already running, we don’t spawn a new process
    server_params = StdioServerParameters(
        command=sys.executable,  # Use the current Python interpreter
        args=["server.py"],      # Run the server script
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("add", arguments={"a": a, "b": b})
            print(f"{a} + {b} = {result.content[0].text}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client-stdio.py <a> <b>")
        sys.exit(1)

    a = int(sys.argv[1])
    b = int(sys.argv[2])
    asyncio.run(main(a, b))
