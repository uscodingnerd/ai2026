from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
import os

# Set OpenAI key
with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
os.environ["OPENAI_API_KEY"] = api_key_str

def calculator_tool(input_str: str) -> str:
    try:
        return str(eval(input_str))  # eval() computes the expression (e.g., "5 + 7 * 2" → 19).
    except Exception as e:
        return f"Error: {str(e)}"

tools = [
    Tool.from_function( # creates a LangChain Tool object from your Python function.
        func=calculator_tool,
        name="Calculator",
        description="Performs math operations. Input should be a Python expression like '3 * (4 + 2)'."
    )
]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)

response = llm.invoke("What's 5 + 7 * 2?")
print(response)

if response.tool_calls:
    tool_call = response.tool_calls[0]
    tool_output = calculator_tool(tool_call['args'].get('input_str', '5 + 7 * 2'))
    print(f"\nCalculation Result: {tool_output}")

