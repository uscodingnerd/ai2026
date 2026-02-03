from langchain_core.prompts import PromptTemplate
import os

# pip install openai langchain langchain_openai
# Set OpenAI key
with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
os.environ["OPENAI_API_KEY"] = api_key_str

prompt = PromptTemplate.from_template(
    "What is the capital of {country}?"
)

output = prompt.invoke({"country": "Canada"})
print(output)
