from fastapi import FastAPI
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter
from src.usecases.search import search

app = FastAPI()
client = QdrantClient(host="localhost", port=6333)  # Qdrantサーバーのホストとポート


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/search/{query}")
async def search(query: str):
    search_result = search(query)
    return search_result
