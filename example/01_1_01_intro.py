from openai import OpenAI

with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
client = OpenAI(
    api_key=api_key_str
)

completion = client.chat.completions.create(
    model="gpt-4o-mini", 
    store=True,
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ]
    # n=2  # request two completions
)

# In most cases, completion.choices contains only one item
print(completion.choices[0].message)
# print(completion.choices[1].message)
