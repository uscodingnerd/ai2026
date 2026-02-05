from langchain_openai import ChatOpenAI
import os
import json

# Set OpenAI key
with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
os.environ["OPENAI_API_KEY"] = api_key_str

movie_titles = ["Inception", "Titanic", "The Matrix", "The Godfather"]

# Load prompts
with open("prompts.txt", "r") as f:
    loaded_prompts = [line.strip() for line in f.readlines()]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Generate in batch
responses = llm.batch(loaded_prompts)  # Returns list of LLM outputs

for title, response in zip(movie_titles, responses):
    print(f"Movie: {title}\nResponse: {response.content.strip()}\n")

results = []
for title, response in zip(movie_titles, responses):
    results.append({
        "title": title,
        "response": response.content.strip()
    })

with open("results.json", "w") as f:
    json.dump(results, f, indent=2)
