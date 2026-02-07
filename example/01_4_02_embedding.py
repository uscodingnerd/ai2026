from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Create embeddings using OpenAI
embedding = OpenAIEmbeddings()

# Initialize Chroma with LangChain
vectorstore = Chroma.from_texts(
    texts=[
        "What is AI?",
        "LangChain is a framework.",
        "Paris is a city."
    ],
    embedding=embedding,
    collection_name="langchain_docs"
)

# Query relevant documents
docs = vectorstore.similarity_search(
    "Tell me about LangChain",
    k=2
)

for doc in docs:
    print(doc.page_content)
