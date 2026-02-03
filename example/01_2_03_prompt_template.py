from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os

# Set OpenAI key
with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
os.environ["OPENAI_API_KEY"] = api_key_str

# ------------------------
# No input prompt
# ------------------------
no_input_prompt = PromptTemplate(
    input_variables=[],
    template="Tell me a joke."
)
print(no_input_prompt.format())
# Output: "Tell me a joke."

# ------------------------
# One input prompt
# ------------------------
one_input_prompt = PromptTemplate(
    input_variables=["adjective"],
    template="Tell me a {adjective} joke."
)
print(one_input_prompt.format(adjective="funny"))
# Output: "Tell me a funny joke."

# ------------------------
# Multiple input prompt
# ------------------------
multiple_input_prompt = PromptTemplate(
    input_variables=["adjective", "content"],
    template="Tell me a {adjective} joke about {content}."
)
print(multiple_input_prompt.format(adjective="funny", content="chickens"))
# Output: "Tell me a funny joke about chickens."



########################################################################################



# ------------------------
# Use LLM with a chain
# ------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Create a chain: PromptTemplate -> LLM
chain = multiple_input_prompt | llm

# Run the chain with **matching input keys**
response = chain.invoke({"adjective": "funny", "content": "chickens"})
print(response.content)  # Use .content to get the LLM output
