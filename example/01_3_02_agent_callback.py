import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage

# Set OpenAI key
with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
os.environ["OPENAI_API_KEY"] = api_key_str


@tool
def calculator_tool(input_str: str) -> str:
    """Evaluate a math input_str like '3 * (4 + 2)'

    Args:
        input_str: The mathematical input_str to evaluate
    """
    try:
        return str(eval(input_str))
    except Exception as e:
        return f"Error: {str(e)}"


tools = [calculator_tool]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)

response = llm.invoke("What's 5 + 7 * 2?")
print("Initial response:")
print(response)
print()

if response.tool_calls:
    tool_call = response.tool_calls[0]

    print(f"Tool call: {tool_call['name']}")
    print(f"Arguments: {tool_call['args']}")

    tool_output = calculator_tool.invoke(tool_call["args"]) # tool_output will be "19" (as a string)
    print(f"Tool output: {tool_output}")
    print()

    messages = [
        ("user", "What's 5 + 7 * 2?"),
        response,  # The AI's response with tool call
        ToolMessage(
            tool_call_id=tool_call["id"],
            content=str(tool_output)  # Ensure it's a string
        )
    ]

    final = llm.invoke(messages)

    print("Final Answer:", final.content)
else:
    print("Final Answer:", response.content)
