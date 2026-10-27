
from langgraph.graph import END, START, StateGraph

from backend.app.graph.nodes import (retrieve_documents, generate_answer,)
from backend.app.graph.state import AssistantState


def build_workflow():

    graph = StateGraph(AssistantState)

    graph.add_node("retrieve_documents", retrieve_documents)
    graph.add_node("generate_answer", generate_answer)

    graph.add_edge(START, "retrieve_documents")
    graph.add_edge("retrieve_documents", "generate_answer")
    graph.add_edge("generate_answer", END)

    return graph.compile()


workflow = build_workflow()
