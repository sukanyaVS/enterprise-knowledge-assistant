
import os

from dotenv import load_dotenv
from langsmith import Client
from langsmith.evaluation import evaluate

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.graph.workflow import workflow

load_dotenv(override=True)

client = Client(
    api_key=os.getenv("LANGSMITH_API_KEY"),
    api_url="https://api.smith.langchain.com",
)

DATASET_NAME = "enterprise-knowledge-assistant-evaluation"


def target(inputs: dict) -> dict:
    """Run a question through the actual LangGraph workflow."""

    result = workflow.invoke({
        "question": inputs["question"]
    })

    return {
        "answer": result.get("answer", ""),
        "has_evidence": result.get("has_evidence", False),
        "documents": result.get("documents", []),
    }


def evaluate_evidence(run, example) -> dict:
    """Check whether the application correctly identifies evidence."""

    expected = example.outputs["expected_evidence"]
    actual = run.outputs["has_evidence"]

    return {
        "key": "evidence_correctness",
        "score": actual == expected,
    }


experiment_results = evaluate(
    target,
    data=DATASET_NAME,
    evaluators=[evaluate_evidence],
    experiment_prefix="initial-rag-evaluation",
    client=client,
)

print("Evaluation completed.")
print(experiment_results)
