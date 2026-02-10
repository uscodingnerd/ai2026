import os
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import streamlit as st

with open("../apikey.txt", "r") as file:
    api_key_str = file.read().strip()
os.environ["OPENAI_API_KEY"] = api_key_str

embedding = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = Chroma(persist_directory="./home_chroma", embedding_function=embedding)


# Setup QA system
@st.cache_resource
def get_retriever_and_llm():
    """Initialize retriever and LLM"""
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return retriever, llm

def answer_question(question, retriever, llm):
    """Answer a question using retrieved context"""
    # Get relevant documents
    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    # Create prompt
    prompt = f"""Answer the question based only on the following context from an insurance contract:

Context:
{context}

Question: {question}

Answer:"""

    # Get answer from LLM
    response = llm.invoke(prompt)

    return response.content, docs


# --- Streamlit UI ---
st.set_page_config(page_title="Insurance Contract QA", page_icon="📄")
st.title("📄 Insurance Contract QA Agent")
st.markdown("Ask questions about your insurance contract and get AI-powered answers with source citations.")

# Add example questions
with st.expander("💡 Example Questions"):
    st.markdown("""
    - What is Insured premises?
    - What is coverage for the food in refrigerator?
    - How much will I get paid if my watch is stolen?
    - What are the coverage limits?
    - What is not covered by this policy?
    """)

query = st.text_input("❓ Your question:", placeholder="e.g., What damages are covered?")

if query:
    with st.spinner("🔍 Searching through the contract..."):
        retriever, llm = get_retriever_and_llm()
        answer, source_docs = answer_question(query, retriever, llm)

        st.success("✅ Answer found!")

        st.subheader("📝 Answer:")
        st.write(answer)

        st.subheader("📚 Source Documents:")
        for i, doc in enumerate(source_docs, 1):
            with st.expander(f"📄 Source Chunk {i}"):
                st.code(doc.page_content.strip(), language="text")
                st.caption(f"Source: {doc.metadata.get('source', 'Unknown')}")

# Add footer
st.markdown("---")
st.caption("Powered by LangChain, OpenAI, and Chroma")
