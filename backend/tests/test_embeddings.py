
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

text = "Employees work from 9 AM to 5 PM, Monday through Friday."

vector = embeddings.embed_query(text)

print("Embedding created successfully!")
print("Vector dimensions:", len(vector))
print("First five values:", vector[:5])
