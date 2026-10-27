# Enterprise Knowledge Assistant

An AI-powered enterprise knowledge assistant built with Python, FastAPI, LangChain, LangGraph, and ChromaDB. The project ingests enterprise documents into a vector store and answers questions using a retrieval-augmented generation (RAG) workflow.

This repository currently focuses on a sample employee handbook and demonstrates how to turn company knowledge into an assistant that can answer grounded questions using source-backed context.

## Features

- Document ingestion and chunking for enterprise knowledge sources
- Vector search with ChromaDB and OpenAI embeddings
- LangGraph workflow for document retrieval and answer generation
- FastAPI application with health checks
- Persistent local vector database for offline experimentation

## Tech Stack

- Python 3.12
- FastAPI
- LangChain / LangGraph
- ChromaDB
- OpenAI embeddings and chat models
- pydantic-settings and python-dotenv

## Project Structure

```text
.
├── backend/
│   └── app/
│       ├── graph/
│       │   ├── nodes.py
│       │   ├── state.py
│       │   └── workflow.py
│       ├── ingestion/
│       │   └── document_loader.py
│       ├── main.py
│       └── retrieval/
│           └── vector_store.py
├── chroma_db/
├── data/
│   └── raw/
│       └── employee_handbook.txt
├── .env.example
├── .env
├── pyproject.toml
├── uv.lock
└── README.md
```

## Getting Started

### 1) Create the environment file

Copy the example environment file and add your OpenAI API key:

```bash
cp .env.example .env
```

Then update `.env` with your credentials:

```env
OPENAI_API_KEY=your-openai-api-key-here
LANGSMITH_TRACING=false
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=enterprise-knowledge-assistant
```

### 2) Install dependencies

Using `uv` is recommended:

```bash
uv sync
```

If you prefer pip instead of `uv`, create a virtual environment and install the dependencies listed in `pyproject.toml` manually.

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install fastapi chromadb langchain langchain-chroma langchain-community langchain-openai langchain-text-splitters langgraph langsmith pydantic-settings pypdf python-dotenv uvicorn[standard]
```

## Ingesting the Knowledge Base

The project includes a vector store builder that loads the employee handbook, splits it into chunks, and stores those chunks in ChromaDB.

Run:

```bash
uv run python -m backend.app.retrieval.vector_store
```

This creates or updates the local vector database under the `chroma_db/` directory.

## Running the API

Start the FastAPI app:

```bash
uv run uvicorn backend.app.main:app --reload
```

The service exposes the following endpoints:

- `GET /` — welcome message
- `GET /health` — health check

Example:

```bash
curl http://127.0.0.1:8000/health
```

## Example RAG Workflow Usage

You can invoke the LangGraph workflow directly from Python:

```python
from backend.app.graph.workflow import workflow

result = workflow.invoke({"question": "What are the working hours?"})
print(result["answer"])
```

This retrieves relevant document chunks from the vector database and generates an answer grounded in the document content.

## Sample Knowledge Source

The default dataset is `data/raw/employee_handbook.txt`, which contains basic HR information such as:

- working hours
- leave policy
- remote work guidance
- IT support process

## Notes

- The assistant is intentionally grounded in the provided knowledge base and should not invent facts.
- ChromaDB persists data locally, so re-running ingestion can refresh the knowledge base with the latest content.
- This project is a starter implementation and can be extended to support more enterprise documents, authentication, and multi-document retrieval.

## License

This project is currently unlicensed unless you add a license file or choose an existing license for distribution.
