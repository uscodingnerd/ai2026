from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)

# Stream output tokens/chunks
for chunk in llm.stream("What is python"):
    print(chunk.content, end="", flush=True)
