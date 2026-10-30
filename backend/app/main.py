
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.app.graph.workflow import workflow


app = FastAPI(
    title="Enterprise Knowledge Assistant API",
    description="API for an AI-powered enterprise knowledge assistant.",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    question: str = Field(
        min_length=1,
        description="Question asked by the user",
    )


class ChatResponse(BaseModel):
    question: str
    answer: str
    has_evidence: bool


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
        result = workflow.invoke(
            {"question": request.question.strip()}
        )

        return ChatResponse(
            question=request.question.strip(),
            answer=result.get("answer", ""),
            has_evidence=result.get("has_evidence", False),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your question.",
        ) from error
