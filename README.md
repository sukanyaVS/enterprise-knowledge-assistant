# Enterprise Knowledge Assistant

An AI-powered assistant that answers questions from enterprise documents using retrieval-augmented generation (RAG). It combines a FastAPI backend, a LangGraph workflow, ChromaDB, OpenAI models, LangSmith tracing/evaluation, and a React chat interface.

## Architecture and design

See [the architecture and design decisions](docs/architecture.md) for the workflow diagram, component roles, and rationale. The original drawing is also available at [architecture.drawio.png](docs/architecture.drawio.png).

| Area | Choice |
| --- | --- |
| Chat model | OpenAI `gpt-4o-mini`, deterministic temperature |
| Embeddings | OpenAI `text-embedding-3-small` |
| Vector store | Persistent local ChromaDB |
| Ingestion | PDF/TXT loaders, 300-character chunks, 50-character overlap |
| Orchestration | LangGraph retrieval → evidence check → answer or abstain |
| API | FastAPI |
| UI | React + TypeScript + Vite |
| Tracing and evaluation | LangSmith |

This is a local-development prototype, not a production deployment. In particular, uploaded files are stored locally and the application sends retrieved text to the configured OpenAI model. Only index documents that are approved for that service.

## Requirements

- Python 3.12+
- Node.js and npm
- OpenAI API key
- LangSmith API key for tracing and evaluation

## Run locally (Windows PowerShell)

1. Configure keys:

   ```powershell
   Copy-Item .env.example .env
   ```

   Add valid `OPENAI_API_KEY` and `LANGSMITH_API_KEY` values to `.env`. Tracing is enabled when the LangSmith key is configured; set `LANGSMITH_TRACING=false` to turn it off.
   `CHROMA_PATH` optionally selects the local ChromaDB directory; its default is `chroma_db` in the repository root.

2. Install backend dependencies and index the sample handbook:

   ```powershell
   uv sync
   uv run python -m backend.app.retrieval.vector_store
   ```

3. Start the API in one terminal:

   ```powershell
   uv run uvicorn backend.app.main:app --reload
   ```

   The API is at `http://127.0.0.1:8000`; interactive API documentation is at `/docs`.

4. Start the UI in another terminal:

   ```powershell
   Set-Location frontend
   npm ci
   npm run dev
   ```

   Open the Vite URL (usually `http://localhost:5173`). Ask a question or upload a PDF/TXT file. Answers include source filenames/pages when available, and the assistant abstains when it cannot find sufficient evidence.

## LangSmith evaluation

The small dataset covers answerable policy questions and questions that should be refused. The evaluators score evidence classification and required answer facts/abstention.

```powershell
uv run python -m backend.evaluation.create_dataset_examples
uv run python -m backend.evaluation.run_evaluation
```

The evaluation runner creates a temporary vector store containing only `data/raw/employee_handbook.txt`; it does not use or upload the regular local ChromaDB contents. It enables tracing for the evaluation run. Check the LangSmith project configured by `LANGSMITH_PROJECT` for traces and experiment results. Evaluation scores are simple exact required-fact checks, not a comprehensive semantic quality measure.

## Tests and checks

```powershell
uv run python -m compileall backend
Set-Location frontend
npm run lint
npm run build
```

The LangGraph chat and LangSmith evaluation require working OpenAI and LangSmith credentials. Do not run them against unapproved documents.

## API endpoints

- `GET /` — service welcome
- `GET /health` — health check
- `POST /chat` — answer a question and return evidence/source references
- `POST /documents/upload` — ingest one PDF or TXT file (maximum 10 MB)

## Sample knowledge source

`data/raw/employee_handbook.txt` contains sample guidance on working hours, leave, remote work, and IT support.
