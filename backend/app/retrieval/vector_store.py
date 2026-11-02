
import hashlib
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from backend.app.ingestion.document_loader import load_and_split_document


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHROMA_PATH = PROJECT_ROOT / "chroma_db"

load_dotenv(PROJECT_ROOT / ".env")


def get_vector_store():
    """Create or connect to the persistent ChromaDB collection."""

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    return Chroma(
        collection_name="employee_handbook",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_PATH),
    )


def ingest_document(file_path: str) -> dict:
    """Load, split, embed, and store a document in ChromaDB."""

    path = Path(file_path).resolve()

    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Document not found: {path}")

    chunks = load_and_split_document(str(path))

    if not chunks:
        raise ValueError("No readable content found in the document.")

    vector_store = get_vector_store()

    source = str(path)

    # Remove previous chunks if this document was already ingested.
    existing = vector_store.get(
        where={"source": source}
    )

    existing_ids = existing.get("ids", [])

    if existing_ids:
        vector_store.delete(ids=existing_ids)

    # Generate stable IDs to avoid duplicate chunks on re-ingestion.
    chunk_ids = []

    for index, chunk in enumerate(chunks):
        unique_text = f"{source}:{index}:{chunk.page_content}"

        chunk_id = hashlib.sha256(
            unique_text.encode("utf-8")
        ).hexdigest()

        chunk_ids.append(chunk_id)

    vector_store.add_documents(
        documents=chunks,
        ids=chunk_ids,
    )

    return {
        "filename": path.name,
        "chunks_processed": len(chunks),
        "previous_chunks_replaced": len(existing_ids),
        "total_chunks_in_database": vector_store._collection.count(),
    }


if __name__ == "__main__":
    sample_file = PROJECT_ROOT / "data" / "raw" / "employee_handbook.txt"

    result = ingest_document(str(sample_file))

    print("Document ingestion completed.")
    print(result)
