import os

from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma

with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
os.environ["OPENAI_API_KEY"] = api_key_str

# Step 1: Load and Chunk the Document
# Load document
loader = TextLoader("insurance_contract.txt", encoding="utf-8")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
documents = splitter.split_documents(docs)


# Step 2: Embed and Store in Chroma Vector Store
embedding = OpenAIEmbeddings(model="text-embedding-3-small")

# Store documents in Chroma
vector_store = Chroma.from_documents(documents, embedding, persist_directory="./home_chroma")

vector_store.persist()
