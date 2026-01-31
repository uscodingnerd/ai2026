import anthropic

with open("../apikey_anthropic.txt", "r") as file:
    api_key_str = file.read().strip()

client = anthropic.Anthropic(api_key=api_key_str)

# Send a message to Claude 4
response = client.messages.create(
    model="claude-sonnet-4-20250514",  # or claude-3-opus-20240229
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Explain quantum computing in simple terms."}
    ]
)

# Print the response
print(response.content[0].text)
