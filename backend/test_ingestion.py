
from backend.app.ingestion.document_loader import load_and_split_document


chunks = load_and_split_document("data/raw/employee_handbook.txt")

print(f"Total chunks created: {len(chunks)}")

for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {index} ---")
    print(chunk.page_content)
    print("Metadata:", chunk.metadata)
