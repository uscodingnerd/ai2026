from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os

# Set OpenAI key
with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
os.environ["OPENAI_API_KEY"] = api_key_str

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

template = "Given the movie title \"{title}\", describe its genre (e.g., sci-fi, romance, action) and a short 2-3 " \
           "sentence plot summary "

movie_titles = ["Inception", "Titanic", "The Matrix", "The Godfather"]

prompt = PromptTemplate(input_variables=["title"], template=template)

batch_inputs = [{"title": t} for t in movie_titles]
formatted_prompts = [prompt.format(**inp) for inp in batch_inputs]

with open("prompts.txt", "w") as f:
    for p in formatted_prompts:
        f.write(p + "\n")
