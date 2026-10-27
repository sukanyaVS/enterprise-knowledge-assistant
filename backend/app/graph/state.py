
from typing import TypedDict

from langchain_core.documents import Document


class AssistantState(TypedDict, total=False):
    question: str
    documents: list[Document]
    answer: str
    is_sufficient: bool
