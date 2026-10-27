
from backend.app.graph.nodes import retrieve_documents


def test_retrieval_node():
    state = {
        "question": "What are the normal working hours?"
    }

    result = retrieve_documents(state)

    documents = result["documents"]

    print(f"Documents retrieved: {len(documents)}")

    for index, document in enumerate(documents, start=1):
        print(f"\n--- Document {index} ---")
        print(document.page_content)
        print("Source:", document.metadata.get("source"))

    assert len(documents) > 0, "No documents were retrieved."


if __name__ == "__main__":
    test_retrieval_node()
