from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
import os

with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
os.environ["OPENAI_API_KEY"] = api_key_str

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Example batch of prompts
prompts = [
    "Tell me a joke about cats.",
    "Tell me a joke about programmers."
]

messages_list = [[HumanMessage(content=prompt)] for prompt in prompts]

# Batch generate responses
responses = llm.batch(messages_list)

for response in responses:
    print(response.content)
    print("-" * 50)
