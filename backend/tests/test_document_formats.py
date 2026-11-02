
from pathlib import Path

from backend.app.ingestion.document_loader import (
    load_and_split_document,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCUMENT_PATH = (
    PROJECT_ROOT / "data" / "raw" / "user_data.pdf"
)


def test_txt_document_loading():
    chunks = load_and_split_document(str(DOCUMENT_PATH))

    print("Document:", DOCUMENT_PATH.name)
    print("Total chunks:", len(chunks))
    print("\nFirst chunk:")
    print(chunks[0].page_content)

    assert len(chunks) > 0


if __name__ == "__main__":
    test_txt_document_loading()
