from openai import OpenAI

with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
client = OpenAI(
    api_key=api_key_str
)

chat_history = [{"role": "system", "content": "You are a helpful assistant that always answers questions with a citation. If the information is not from a real source, invent a credible-sounding fictional one."}]

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

    with open("chat_log.txt", "a", encoding="utf-8") as f:
        f.write(f"User: {user_input}\n")
        f.write(f"Assistant: {reply}\n\n")
