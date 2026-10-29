
from langgraph.graph import END, START, StateGraph

from backend.app.graph.nodes import (
    abstain,
    check_evidence,
    generate_answer,
    retrieve_documents,
)
from backend.app.graph.state import AssistantState


def build_workflow():
    """Build the evidence-aware RAG workflow."""

    graph = StateGraph(AssistantState)

    graph.add_node("retrieve_documents", retrieve_documents)
    graph.add_node("check_evidence", check_evidence)
    graph.add_node("generate_answer", generate_answer)
    graph.add_node("abstain", abstain)

    graph.add_edge(START, "retrieve_documents")
    graph.add_edge("retrieve_documents", "check_evidence")

    graph.add_conditional_edges(
        "check_evidence",
        lambda state: (
            "generate_answer"
            if state.get("has_evidence", False)
            else "abstain"
        ),
        {
            "generate_answer": "generate_answer",
            "abstain": "abstain",
        },
    )

    graph.add_edge("generate_answer", END)
    graph.add_edge("abstain", END)

    return graph.compile()


workflow = build_workflow()
