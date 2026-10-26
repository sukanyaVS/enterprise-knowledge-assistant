
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_PATH = PROJECT_ROOT / "chroma_db"

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_store = Chroma(
    collection_name="employee_handbook",
    embedding_function=embeddings,
    persist_directory=str(CHROMA_PATH),
)

question = "What are the normal working hours?"

results = vector_store.similarity_search_with_score(
    question,
    k=3,
)

for index, (document, score) in enumerate(results, start=1):
    print(f"\n--- Result {index} ---")
    print("Text:", document.page_content)
    print("Source:", document.metadata.get("source"))
    print("Distance:", score)
