from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
import os

# --- Set OpenAI key ---
with open("../apikey.txt", "r") as file:
    os.environ["OPENAI_API_KEY"] = file.read().strip()

# --- NumToWords tool ---
NUM_DICT = {
    0: '', 1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five',
    6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten',
    11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen',
    15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen',
    19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty',
    50: 'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty', 90: 'Ninety'
}

def dfs(num: int) -> str:
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

@tool
def NumToWords(num_str: str) -> str:
    """Convert a number into English words."""
    num = int(num_str)
    if num == 0:
        return "Zero"
    return dfs(num)

@tool
def SquareNumber(num_str: str) -> str:
    """Return the square of a number."""
    num = int(num_str)
    return str(num * num)

# --- Tools dictionary ---
tools = [NumToWords, SquareNumber]
tool_map = {tool.name: tool for tool in tools}

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use tools when appropriate."),
    ("user", "{input}")
])

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
).bind_tools(tools)

query = "Calculate 4 square"
#query = "Convert 458 to words"

prompt_value = prompt.format_prompt(input=query)

response = llm.invoke(prompt_value)

print("\nQuery:", query)
print("Raw LLM response:", response)

if response.tool_calls:
    call = response.tool_calls[0]
    tool_name = call["name"]
    tool_args = call["args"]

    print("\nTool selected by LLM:", tool_name)
    print("Tool arguments:", tool_args)

    result = tool_map[tool_name].invoke(tool_args)
    print("Tool result:", result)

else:
    print("\nLLM response (no tool used):", response.content)
