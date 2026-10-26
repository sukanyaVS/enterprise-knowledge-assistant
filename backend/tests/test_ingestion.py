
from backend.app.ingestion.document_loader import load_and_split_document
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
chunks = load_and_split_document(
    str(PROJECT_ROOT / "data" / "raw" / "employee_handbook.txt")
)

print(f"Total chunks created: {len(chunks)}")

for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {index} ---")
    print(chunk.page_content)
    print("Metadata:", chunk.metadata)
