
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.app.graph.workflow import workflow
from backend.app.retrieval.vector_store import ingest_document
from typing import Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
UPLOAD_DIRECTORY = PROJECT_ROOT / "data" / "raw"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


app = FastAPI(
    title="Enterprise Knowledge Assistant API",
    description="API for an AI-powered enterprise knowledge assistant.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str = Field(
        min_length=1,
        description="Question asked by the user",
    )


class SourceReference(BaseModel):
    filename: str
    page: Optional[int] = None


class ChatResponse(BaseModel):
    question: str
    answer: str
    has_evidence: bool
    sources: list[SourceReference] = Field(default_factory=list)


@app.get("/")
def root():
    return {
        "message": "Enterprise Knowledge Assistant API is running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        question = request.question.strip()

        if not question:
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty.",
            )

        result = workflow.invoke({"question": question})

        # Extract source references from retrieved documents
        sources = []
        seen_sources = set()

        for document in result.get("documents", []):
            metadata = document.metadata

            source_path = metadata.get("source", "")
            filename = (
                Path(source_path).name
                if source_path
                else "Unknown"
            )

            page = metadata.get("page")

            source_key = (filename, page)

            if source_key not in seen_sources:
                sources.append(
                    SourceReference(
                        filename=filename,
                        page=page,
                    )
                )
                seen_sources.add(source_key)

        has_evidence = result.get("has_evidence", False)

        return ChatResponse(
            question=question,
            answer=result.get("answer", ""),
            has_evidence=has_evidence,
            sources=sources if has_evidence else [],
        )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your question.",
        ) from error

@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    original_filename = file.filename or ""
    filename = original_filename.replace("\\", "/").split("/")[-1]

    if not filename or filename in {".", ".."}:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename.",
        )

    extension = Path(filename).suffix.lower()

    if extension not in {".pdf", ".txt"}:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported.",
        )

    file_content = await file.read(MAX_FILE_SIZE + 1)

    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size cannot exceed 10 MB.",
        )

    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

    file_path = UPLOAD_DIRECTORY / filename

    try:
        file_path.write_bytes(file_content)

        result = ingest_document(str(file_path))

        return {
            "message": "Document uploaded and indexed successfully.",
            **result,
        }

    except (ValueError, FileNotFoundError) as error:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Document ingestion failed.",
        ) from error

    finally:
        await file.close()
