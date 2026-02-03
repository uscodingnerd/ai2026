from openai import OpenAI

with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
client = OpenAI(
    api_key=api_key_str
)

completion = client.chat.completions.create(
    model="gpt-4o-mini", # GPT-4o-mini is a smaller, optimized variant of GPT-4o, OpenAI’s flagship multimodal model.
    store=True,
    messages=[
        {"role": "user", "content": "What is the capital of France?"} # What is python?
    ]
    # n=2  # request two completions
)

print(completion.choices[0].message)
