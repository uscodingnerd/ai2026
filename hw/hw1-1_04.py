from openai import OpenAI
import streamlit as st

with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
client = OpenAI(
    api_key=api_key_str
)

st.set_page_config(page_title="ChatGPT Web Interface", page_icon="💬") # icon for the website
st.title("💬 ChatGPT Web Interface")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a friendly assistant who helps users learn programming."}
    ]

user_input = st.text_input("You:", key="user_input")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.spinner("ChatGPT is thinking..."):
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=st.session_state["messages"]
        )

    reply = completion.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": reply})

for msg in st.session_state["messages"][1:]:  # Skip the system message in line 20
    speaker = "👤 You" if msg["role"] == "user" else "🤖 Assistant"
    st.markdown(f"**{speaker}:** {msg['content']}")
