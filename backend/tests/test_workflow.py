
from backend.app.graph.workflow import workflow


def test_workflow():
    initial_state = {
        "question": "What are the normal working hours?"
    }

    result = workflow.invoke(initial_state)

    print("Question:", result["question"])
    print("Documents retrieved:", len(result["documents"]))
    print("\nGenerated answer:")
    print(result["answer"])

    assert result["question"] == initial_state["question"]
    assert len(result["documents"]) > 0
    assert isinstance(result["answer"], str)
    assert result["answer"].strip()


if __name__ == "__main__":
    test_workflow()
