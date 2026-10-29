
from backend.app.graph.workflow import workflow


def test_answerable_question():
    question = "What are the normal working hours?"

    result = workflow.invoke({"question": question})

    print("\n--- Answerable Question ---")
    print("Question:", result["question"])
    print("Documents retrieved:", len(result.get("documents", [])))
    print("Evidence sufficient:", result.get("has_evidence"))
    print("Evidence reason:", result.get("evidence_reason"))
    print("Answer:", result.get("answer"))

    assert result.get("has_evidence") is True
    assert len(result.get("documents", [])) > 0
    assert result.get("answer", "").strip()


def test_unanswerable_question():
    question = "What is the company's stock ticker?"

    result = workflow.invoke({"question": question})

    print("\n--- Unanswerable Question ---")
    print("Question:", result["question"])
    print("Documents retrieved:", len(result.get("documents", [])))
    print("Evidence sufficient:", result.get("has_evidence"))
    print("Evidence reason:", result.get("evidence_reason"))
    print("Answer:", result.get("answer"))

    assert result.get("has_evidence") is False
    assert "couldn't find enough information" in (
        result.get("answer", "").lower()
    )


if __name__ == "__main__":
    test_answerable_question()
    test_unanswerable_question()
