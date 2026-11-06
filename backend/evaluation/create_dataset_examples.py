
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langsmith import Client


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(PROJECT_ROOT / ".env")

DATASET_NAME = "enterprise-knowledge-assistant-evaluation"

examples = [
    {
        "inputs": {"question": "What are the normal working hours?"},
        "outputs": {
            "expected_answer": "The normal working hours are 9:00 AM to 6:00 PM, Monday through Friday.",
            "expected_evidence": True,
            "required_facts": ["9:00 AM", "6:00 PM", "Monday through Friday"],
        },
    },
    {
        "inputs": {"question": "When does the workday begin and end?"},
        "outputs": {
            "expected_answer": "The normal working hours are 9:00 AM to 6:00 PM, Monday through Friday.",
            "expected_evidence": True,
            "required_facts": ["9:00 AM", "6:00 PM", "Monday through Friday"],
        },
    },
    {
        "inputs": {"question": "How do employees request planned leave?"},
        "outputs": {
            "expected_answer": "Employees request planned leave through the company's leave management system. Managers review requests based on team availability.",
            "expected_evidence": True,
            "required_facts": ["leave management system", "team availability"],
        },
    },
    {
        "inputs": {"question": "How can employees get technical assistance?"},
        "outputs": {
            "expected_answer": "Employees should contact the IT support team through the internal help desk portal.",
            "expected_evidence": True,
            "required_facts": ["IT support team", "internal help desk portal"],
        },
    },
    {
        "inputs": {"question": "What is the current stock price of Apple?"},
        "outputs": {"expected_evidence": False},
    },
    {
        "inputs": {"question": "Who won the last FIFA World Cup?"},
        "outputs": {"expected_evidence": False},
    },
    {
        "inputs": {"question": "What is the company's parental leave duration?"},
        "outputs": {"expected_evidence": False},
    },
]


def main() -> None:
    api_key = os.getenv("LANGSMITH_API_KEY")
    if not api_key:
        raise RuntimeError("LANGSMITH_API_KEY must be configured in .env.")

    client = Client(
        api_key=api_key,
        api_url=os.getenv(
            "LANGSMITH_ENDPOINT", "https://api.smith.langchain.com"
        ),
    )

    if not client.has_dataset(dataset_name=DATASET_NAME):
        client.create_dataset(
            dataset_name=DATASET_NAME,
            description=(
                "Answerable and unanswerable questions over the sample "
                "employee handbook."
            ),
        )

    existing = {
        example.inputs.get("question"): example
        for example in client.list_examples(dataset_name=DATASET_NAME)
    }

    added = 0
    updated = 0
    for example in examples:
        question = example["inputs"]["question"]
        current = existing.get(question)
        if current is None:
            client.create_example(
                dataset_name=DATASET_NAME,
                inputs=example["inputs"],
                outputs=example["outputs"],
            )
            added += 1
        elif current.outputs != example["outputs"]:
            client.update_example(
                example_id=current.id,
                inputs=example["inputs"],
                outputs=example["outputs"],
            )
            updated += 1

    print(
        f"Dataset '{DATASET_NAME}' ready: "
        f"{len(examples)} examples ({added} added, {updated} updated)."
    )


if __name__ == "__main__":
    main()
