from openai import OpenAI

with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
client = OpenAI(
    api_key=api_key_str
)

chat_history = [{"role": "system", "content": "You are a friendly assistant who helps users learn programming."}]

while True:
    user_input = input("User: ")
    chat_history.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=chat_history
    )

    reply = completion.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})
    print("Assistant:", reply)
