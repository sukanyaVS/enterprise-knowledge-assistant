import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from langsmith import Client
from langsmith.evaluation import evaluate


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

DATASET_NAME = "enterprise-knowledge-assistant-evaluation"


def evaluate_evidence(run, example) -> dict:
    """Check whether the application correctly identifies evidence."""

    expected = bool(example.outputs["expected_evidence"])
    actual = bool(run.outputs["has_evidence"])

    return {
        "key": "evidence_correctness",
        "score": actual == expected,
    }


def evaluate_answer(run, example) -> dict:
    """Check required answer facts or abstention for unsupported questions."""

    answer = str(run.outputs.get("answer", "")).casefold()
    expected_evidence = bool(example.outputs["expected_evidence"])
    if expected_evidence:
        required_facts = example.outputs.get("required_facts", [])
        score = bool(required_facts) and all(
            fact.casefold() in answer for fact in required_facts
        )
    else:
        score = "couldn't find enough information" in answer

    return {
        "key": "answer_quality",
        "score": score,
    }


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY must be configured in .env.")
    api_key = os.getenv("LANGSMITH_API_KEY")
    if not api_key:
        raise RuntimeError("LANGSMITH_API_KEY must be configured in .env.")

    client = Client(
        api_key=api_key,
        api_url=os.getenv(
            "LANGSMITH_ENDPOINT", "https://api.smith.langchain.com"
        ),
    )

    # Keep evaluation isolated from the local index, which may contain
    # uploaded or personal documents.
    with tempfile.TemporaryDirectory(prefix="eka-evaluation-") as chroma_path:
        os.environ["CHROMA_PATH"] = chroma_path
        os.environ["LANGSMITH_TRACING"] = "true"

        from backend.app.retrieval.vector_store import ingest_document
        from backend.app.graph.workflow import build_workflow

        handbook = PROJECT_ROOT / "data" / "raw" / "employee_handbook.txt"
        ingest_document(str(handbook))
        workflow = build_workflow()

        def target(inputs: dict) -> dict:
            result = workflow.invoke({"question": inputs["question"]})
            return {
                "answer": result.get("answer", ""),
                "has_evidence": result.get("has_evidence", False),
            }

        results = evaluate(
            target,
            data=DATASET_NAME,
            evaluators=[evaluate_evidence, evaluate_answer],
            experiment_prefix="handbook-rag-evaluation",
            client=client,
            max_concurrency=1,
        )

    print("Evaluation completed.")
    print(results)


if __name__ == "__main__":
    main()
