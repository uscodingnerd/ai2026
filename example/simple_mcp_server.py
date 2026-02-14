import sys
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio
import asyncio


def log(message):
    print(f"[MCP SERVER] {message}", file=sys.stderr, flush=True)


# --- NumToWords Implementation ---
NUM_DICT = {
    0: '', 1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five',
    6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten',
    11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen',
    15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen',
    19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty',
    50: 'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty', 90: 'Ninety'
}


def dfs(num: int) -> str:
    """Recursive helper to convert numbers to words"""
    if num < 20:
        return NUM_DICT[num]
    elif num < 100:
        return (NUM_DICT[num // 10 * 10] + ' ' + dfs(num % 10)).strip()
    elif num < 1000:
        return (NUM_DICT[num // 100] + ' Hundred ' + dfs(num % 100)).strip()
    elif num < 1_000_000:
        return (dfs(num // 1000) + ' Thousand ' + dfs(num % 1000)).strip()
    elif num < 1_000_000_000:
        return (dfs(num // 1_000_000) + ' Million ' + dfs(num % 1_000_000)).strip()
    elif num < 1_000_000_000_000:
        return (dfs(num // 1_000_000_000) + ' Billion ' + dfs(num % 1_000_000_000)).strip()
    return ''


def num_to_words(num: int) -> str:
    """Convert a number into English words"""
    if num == 0:
        return "Zero"
    return dfs(num)


def square_number(num: int) -> int:
    """Return the square of a number"""
    return num * num


# Create server instance
app = Server("number-tools-server")
log("Number Tools Server instance created")


# Define tools
@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    log("list_tools() called - returning NumToWords and SquareNumber tools")
    return [
        Tool(
            name="NumToWords",
            description="Convert a number into English words. For example, 123 becomes 'One Hundred Twenty Three'",
            inputSchema={
                "type": "object",
                "properties": {
                    "number": {
                        "type": "integer",
                        "description": "The number to convert to words (e.g., 458, 1234)"
                    }
                },
                "required": ["number"]
            }
        ),
        Tool(
            name="SquareNumber",
            description="Calculate the square of a number. Returns number * number",
            inputSchema={
                "type": "object",
                "properties": {
                    "number": {
                        "type": "integer",
                        "description": "The number to square (e.g., 4, 25)"
                    }
                },
                "required": ["number"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution"""
    log(f"call_tool() called - tool: {name}, arguments: {arguments}")

    if name == "NumToWords":
        number = arguments["number"]
        result = num_to_words(number)
        log(f"NumToWords({number}) returning: {result}")
        return [TextContent(
            type="text",
            text=result
        )]

    elif name == "SquareNumber":
        number = arguments["number"]
        result = square_number(number)
        log(f"SquareNumber({number}) returning: {result}")
        return [TextContent(
            type="text",
            text=str(result)
        )]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the MCP server"""
    log("Starting Number Tools MCP server...")
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        log("Server streams established, running app...")
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    log("Number Tools MCP Server starting up...")
    asyncio.run(main())
    log("Number Tools MCP Server shut down")
