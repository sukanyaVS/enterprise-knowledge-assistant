
import os
from dotenv import load_dotenv
from langsmith import Client

load_dotenv(override=True)

client = Client(
    api_key=os.getenv("LANGSMITH_API_KEY"),
    api_url="https://api.smith.langchain.com",
)

DATASET_NAME = "enterprise-knowledge-assistant-evaluation"

examples = [
    {
        "inputs": {
            "question": "What are the normal working hours?"
        },
        "outputs": {
            "expected_answer": (
                "The normal working hours are 9:00 AM to "
                "6:00 PM, Monday through Friday."
            ),
            "expected_evidence": True,
        },
    },
    {
        "inputs": {
            "question": "When does the workday begin and end?"
        },
        "outputs": {
            "expected_answer": (
                "The normal working hours are 9:00 AM to "
                "6:00 PM, Monday through Friday."
            ),
            "expected_evidence": True,
        },
    },
    {
        "inputs": {
            "question": "What is the current stock price of Apple?"
        },
        "outputs": {
            "expected_evidence": False,
        },
    },
    {
        "inputs": {
            "question": "Who won the last FIFA World Cup?"
        },
        "outputs": {
            "expected_evidence": False,
        },
    },
]

# Check whether examples already exist to avoid duplicates.
existing = list(
    client.list_examples(dataset_name=DATASET_NAME)
)

existing_questions = {
    example.inputs.get("question")
    for example in existing
}

added = 0

for example in examples:
    question = example["inputs"]["question"]

    if question not in existing_questions:
        client.create_example(
            dataset_name=DATASET_NAME,
            inputs=example["inputs"],
            outputs=example["outputs"],
        )
        added += 1

print(f"Added {added} new examples.")
print(f"Dataset now contains {len(existing) + added} examples.")
