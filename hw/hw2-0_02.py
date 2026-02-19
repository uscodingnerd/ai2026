import anthropic

with open("../apikey_anthropic.txt") as f:
    api_key = f.read().strip()

with open("SKILL.md") as f:
    skill_instructions = f.read()

client = anthropic.Anthropic(api_key=api_key)

# --- Define the MCP tools to Claude ---
tools = [
    {
        "name": "NumToWords",
        "description": "Convert a number into English words. e.g. 123 → 'One Hundred Twenty Three'",
        "input_schema": {
            "type": "object",
            "properties": {
                "number": {"type": "integer", "description": "The number to convert"}
            },
            "required": ["number"]
        }
    },
    {
        "name": "SquareNumber",
        "description": "Calculate the square of a number. Returns number * number",
        "input_schema": {
            "type": "object",
            "properties": {
                "number": {"type": "integer", "description": "The number to square"}
            },
            "required": ["number"]
        }
    }
]

# --- Your local tool executor (calls your MCP logic directly) ---
def execute_tool(name, arguments):
    if name == "NumToWords":
        number = arguments["number"]
        from simple_mcp_server import num_to_words
        return num_to_words(number)
    elif name == "SquareNumber":
        number = arguments["number"]
        from simple_mcp_server import square_number
        return str(square_number(number))
    raise ValueError(f"Unknown tool: {name}")

# --- Agentic loop ---
def run(user_message):
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            system=skill_instructions,   # SKILL.md guides behavior
            tools=tools,                  # MCP tools registered here
            messages=messages
        )

        # Claude is done — print final text response
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    print(block.text)
            break

        # Claude wants to call a tool
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"→ Calling tool: {block.name}({block.input})")
                    result = execute_tool(block.name, block.input)
                    print(f"← Result: {result}")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            messages.append({"role": "user", "content": tool_results})
            # Loop continues — Claude sees the result and responds

# --- Run it ---
# run("Square 12 and then convert it to words")
# run("Square word 12")
run("Word Square 13")
# run("Square 12")

# User: "Convert 4582 to words"
#     ↓
# Claude reads SKILL.md (knows what to do)
# Claude sees tools available (knows what it can call)
#     ↓
# Claude returns tool_use: NumToWords(4582)
#     ↓
# Your execute_tool() runs it → "Four Thousand Five Hundred Eighty Two"
#     ↓
# You send tool_result back to Claude
#     ↓
# Claude formats final response per SKILL.md instructions
