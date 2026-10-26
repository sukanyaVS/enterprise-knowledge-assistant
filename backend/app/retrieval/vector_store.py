
import hashlib
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from backend.app.ingestion.document_loader import load_and_split_document


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DOCUMENT_PATH = (
    PROJECT_ROOT / "data" / "raw" / "employee_handbook.txt"
)
CHROMA_PATH = PROJECT_ROOT / "chroma_db"

load_dotenv(PROJECT_ROOT / ".env")


def create_vector_store():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_store = Chroma(
        collection_name="employee_handbook",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_PATH),
    )

    source = str(DOCUMENT_PATH.resolve())

    chunks = load_and_split_document(source)

    existing = vector_store.get(
        where={"source": source}
    )
    existing_ids = existing.get("ids", [])

    if existing_ids:
        vector_store.delete(ids=existing_ids)

    chunk_ids = []

    for index, chunk in enumerate(chunks):
        unique_text = f"{source}:{index}:{chunk.page_content}"
        chunk_id = hashlib.sha256(
            unique_text.encode("utf-8")
        ).hexdigest()

        chunk_ids.append(chunk_id)

    if chunks:
        vector_store.add_documents(
            documents=chunks,
            ids=chunk_ids,
        )

    print("Document ingestion completed.")
    print(f"Chunks processed: {len(chunks)}")
    print(f"Previous chunks replaced: {len(existing_ids)}")
    print(f"Chunks currently stored: {vector_store._collection.count()}")
    print(f"Database location: {CHROMA_PATH}")

    return vector_store


if __name__ == "__main__":
    create_vector_store()
