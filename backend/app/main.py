from fastapi import FastAPI

app = FastAPI(
    title="Enterprise Knowledge Assistant API",
    description="API for an AI-powered enterprise knowledge assistant.",
    version="1.0.0",
)

@app.get("/")
def root():
    return {
        "message": "Enterprise Knowledge Assistant API is running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}