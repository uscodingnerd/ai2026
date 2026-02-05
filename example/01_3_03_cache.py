import time
import os

from langchain_community.cache import SQLiteCache
from langchain_openai import OpenAI
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache

with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
os.environ["OPENAI_API_KEY"] = api_key_str

set_llm_cache(InMemoryCache())

llm = OpenAI(model_name="gpt-4o-mini", n=2, best_of=2)

s1 = time.perf_counter()
llm.invoke("Tell me a joke")
elapsed1 = time.perf_counter() - s1
print(f"\033[1mexecuted first in {elapsed1:.2f} seconds.\033[0m")

s2 = time.perf_counter()
llm.invoke("Tell me a joke")
elapsed2 = time.perf_counter() - s2
print(f"\033[1mexecuted second in {elapsed2:.2f} seconds.\033[0m")
