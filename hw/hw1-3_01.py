from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache
from langchain_community.cache import InMemoryCache, SQLiteCache
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
import time

# Set OpenAI key
with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
os.environ["OPENAI_API_KEY"] = api_key_str

NUM_DICT = {
    0: '',
    1: 'One',
    2: 'Two',
    3: 'Three',
    4: 'Four',
    5: 'Five',
    6: 'Six',
    7: 'Seven',
    8: 'Eight',
    9: 'Nine',
    10: 'Ten',
    11: 'Eleven',
    12: 'Twelve',
    13: 'Thirteen',
    14: 'Fourteen',
    15: 'Fifteen',
    16: 'Sixteen',
    17: 'Seventeen',
    18: 'Eighteen',
    19: 'Nineteen',
    20: 'Twenty',
    30: 'Thirty',
    40: 'Forty',
    50: 'Fifty',
    60: 'Sixty',
    70: 'Seventy',
    80: 'Eighty',
    90: 'Ninety',
}


def dfs(num: int) -> str:
    if num < 20:
        return NUM_DICT[num]
    elif num < 100:
        return (NUM_DICT[num // 10 * 10] + ' ' + dfs(num % 10)).strip()
    elif num < 1000:
        return (NUM_DICT[num // 100] + ' Hundred ' + dfs(num % 100)).strip()
    elif num < 1000000:
        return (dfs(num // 1000) + ' Thousand ' + dfs(num % 1000)).strip()
    elif num < 1000000000:
        return (dfs(num // 1000000) + ' Million ' + dfs(num % 1000000)).strip()
    elif num < 1000000000000:
        return (dfs(num // 1000000000) + ' Billion ' + dfs(num % 1000000000)).strip()
    return ''


def num_to_words_tool(num_str: str) -> str:
    try:
        num = int(num_str)
        if num == 0:
            return 'Zero'
        return dfs(num)
    except Exception as e:
        return f"Error: {str(e)}"


# Tool: Web search
tools = [
    Tool(
        name="NumToWords",
        func=num_to_words_tool,
        description="Converts numbers like 2024 into English words like 'two thousand twenty-four"
    )
]

# --- LLM and Prompt ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

set_llm_cache(SQLiteCache(database_path=".langchain_cache.db"))
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
).bind_tools(tools)

tool_map = {tool.name: tool for tool in tools}

# --- Run Agent ---
query = "convert 458 to words"
prompt_value = prompt.format_prompt(input=query)

# ---------------- First Call ----------------
start = time.time()
response1 = llm.invoke(prompt_value)
end = time.time()

print("\n--- First Call ---")
print("Raw LLM response:", response1)

if response1.tool_calls:
    call = response1.tool_calls[0]
    tool_name = call["name"]
    tool_args = call["args"]

    if "__arg1" in tool_args:
        result = tool_map[tool_name].func(tool_args["__arg1"])
    else:
        result = tool_map[tool_name].func(**tool_args)
    print("Tool invoked:", tool_name)
    print("Tool output:", result)
else:
    print("LLM output:", response1.content)

print(f"Execution time: {end - start:.3f}s")

# ---------------- Second Call (Cached) ----------------
start = time.time()
response2 = llm.invoke(prompt_value)
end = time.time()

print("\n--- Second Call (Cache Hit) ---")
print("Raw LLM response:", response2)

if response2.tool_calls:
    call = response2.tool_calls[0]
    tool_name = call["name"]
    tool_args = call["args"]

    if "__arg1" in tool_args:
        result = tool_map[tool_name].func(tool_args["__arg1"])
    else:
        result = tool_map[tool_name].func(**tool_args)
    print("Tool invoked:", tool_name)
    print("Tool output:", result)
else:
    print("LLM output:", response2.content)

print(f"Execution time: {end - start:.3f}s")

