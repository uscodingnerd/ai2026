from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os

# Set OpenAI key
with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()

os.environ["OPENAI_API_KEY"] = api_key_str

# Define the prompt
prompt = PromptTemplate.from_template("What is the capital of {country}?")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

chain = prompt | llm

response = chain.invoke({"country": "Canada"})
print(response.content)
