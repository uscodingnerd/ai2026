import sys
import os
from mcp.server import Server
from mcp.types import Tool, TextContent, Resource
import mcp.server.stdio
import asyncio
from pathlib import Path

# Import LangChain components
try:
    from langchain_community.vectorstores import Chroma
    from langchain_openai import OpenAIEmbeddings
except ImportError as e:
    print(f"[MCP SERVER] ERROR: Missing dependencies: {e}", file=sys.stderr)
    print("[MCP SERVER] Install with: pip install langchain langchain-community langchain-openai chromadb",
          file=sys.stderr)
    sys.exit(1)


# Debug logging function
def log(message):
    """Log to stderr so it appears in Claude Desktop logs"""
    print(f"[MCP SERVER] {message}", file=sys.stderr, flush=True)


# --- Configuration ---
try:
    with open(r"G:\MyFiles\Coding\Python\AI\apikey.txt", "r") as file:
        api_key_str = file.read().strip()
    os.environ["OPENAI_API_KEY"] = api_key_str
    log("OpenAI API key loaded successfully")
except FileNotFoundError:
    log("WARNING: apikey.txt not found. Set OPENAI_API_KEY environment variable instead.")
except Exception as e:
    log(f"ERROR loading API key: {e}")

# Initialize embeddings and vector store
log("Initializing embeddings and vector store...")
try:
    embedding = OpenAIEmbeddings(model="text-embedding-3-small")
    # Make sure use the absolute path
    vector_store = Chroma(persist_directory=r"G:\MyFiles\Coding\Python\AI\hw\home_chroma", embedding_function=embedding)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    log("Vector store loaded successfully")
except Exception as e:
    log(f"ERROR initializing vector store: {e}")
    retriever = None

# Create server instance
app = Server("insurance-qa-server")
log("Insurance QA Server instance created")


def answer_question(question: str) -> tuple[str, list]:
    """Answer a question using retrieved context from insurance contract"""
    if retriever is None:
        return "Error: Vector store not initialized", []

    try:
        # Get relevant documents
        docs = retriever.invoke(question)
        log(f"Retrieved {len(docs)} documents for question: {question}")

        # Combine context
        context = "\n\n".join([doc.page_content for doc in docs])

        # Format the answer with sources
        answer_parts = ["Based on the insurance contract:\n"]

        # Add main context
        answer_parts.append(context)

        # Add source information
        answer_parts.append("\n\nSource documents:")
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get('source', 'Unknown')
            answer_parts.append(f"\n{i}. {source}")

        answer = "\n".join(answer_parts)

        return answer, docs

    except Exception as e:
        log(f"ERROR answering question: {e}")
        return f"Error processing question: {str(e)}", []


# Define tools
@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    log("list_tools() called - returning InsuranceQA tool")
    return [
        Tool(
            name="InsuranceQA",
            description="Answer questions about an insurance contract using RAG (Retrieval-Augmented Generation). Searches through the insurance contract document and provides answers with source citations. Use this for questions about coverage, limits, exclusions, definitions, or any insurance policy details.",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question to ask about the insurance contract (e.g., 'What is covered?', 'What are the coverage limits?', 'What is not covered?')"
                    }
                },
                "required": ["question"]
            }
        ),
        Tool(
            name="SearchInsuranceContract",
            description="Search the insurance contract for specific terms or concepts and return relevant passages. Use this when you need to find specific information in the contract.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query or topic (e.g., 'insured premises', 'coverage limits', 'exclusions')"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of relevant passages to return (default: 3)",
                        "default": 3
                    }
                },
                "required": ["query"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution"""
    log(f"call_tool() called - tool: {name}, arguments: {arguments}")

    if name == "InsuranceQA":
        question = arguments["question"]
        answer, docs = answer_question(question)
        log(f"InsuranceQA answered question with {len(docs)} source documents")
        return [TextContent(type="text", text=answer)]

    elif name == "SearchInsuranceContract":
        query = arguments["query"]
        num_results = arguments.get("num_results", 3)

        if retriever is None:
            return [TextContent(type="text", text="Error: Vector store not initialized")]

        try:
            # Update search kwargs for this query
            custom_retriever = vector_store.as_retriever(search_kwargs={"k": num_results})
            docs = custom_retriever.invoke(query)
            log(f"SearchInsuranceContract found {len(docs)} results for: {query}")

            # Format results
            result_parts = [f"Found {len(docs)} relevant passages for '{query}':\n"]
            for i, doc in enumerate(docs, 1):
                result_parts.append(f"\n--- Passage {i} ---")
                result_parts.append(doc.page_content.strip())
                source = doc.metadata.get('source', 'Unknown')
                result_parts.append(f"(Source: {source})\n")

            result = "\n".join(result_parts)
            return [TextContent(type="text", text=result)]

        except Exception as e:
            log(f"ERROR in SearchInsuranceContract: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    raise ValueError(f"Unknown tool: {name}")


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources"""
    log("list_resources() called")
    return [
        Resource(
            uri="insurance://contract/info",
            name="Insurance Contract Information",
            mimeType="text/plain",
            description="Information about the loaded insurance contract and vector store"
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read resource content"""
    log(f"read_resource() called - uri: {uri}")

    if uri == "insurance://contract/info":
        if retriever is None:
            return "Vector store not initialized. Check logs for errors."

        try:
            # Get some stats about the vector store
            collection = vector_store._collection
            count = collection.count()

            info = f"""Insurance Contract QA System

Vector Store Status: Loaded
Database Location: ./home_chroma
Embedding Model: text-embedding-3-small
Total Document Chunks: {count}

Available Tools:
1. InsuranceQA - Ask questions about the insurance contract
2. SearchInsuranceContract - Search for specific terms or passages

Example Questions:
- What is insured premises?
- What is coverage for the food in refrigerator?
- How much will I get paid if my watch is stolen?
- What are the coverage limits?
- What is not covered by this policy?
"""
            return info
        except Exception as e:
            return f"Error retrieving contract info: {str(e)}"

    raise ValueError(f"Unknown resource: {uri}")


async def main():
    """Run the MCP server"""
    log("Starting Insurance QA MCP server...")
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        log("Server streams established, running app...")
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    log("Insurance QA MCP Server starting up...")
    asyncio.run(main())
    log("Insurance QA MCP Server shut down")
