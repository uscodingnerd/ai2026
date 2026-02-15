import anthropic

with open("../apikey_anthropic.txt", "r") as file:
    api_key_str = file.read().strip()

client = anthropic.Anthropic(api_key=api_key_str)

code = """
def num_to_words_tool(num_str: str) -> str:
    try:
        num = int(num_str)
        if num == 0:
            return 'Zero'
        return dfs(num)
    except Exception as e:
        return f"Error: {str(e)}"
"""

with open("SKILL.md", "r") as f:
    skill_instructions = f.read()

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=skill_instructions,
    messages=[
        {"role": "user", "content": f"Summarize this code:\n\n{code}"}
    ]
)

print(response.content[0].text)
