import os
from openai import OpenAI
from src import constants
from qdrant_client import QdrantClient

qdrant_collection = "langchain-docs-semanticsearch-dev-0-2-0"
search_limit_n = 2


# content -> embedding
def embedding(content: str) -> list[float]:
    api_key = os.getenv(constants.ENV_OPENAI_API_KEY)
    client = OpenAI(api_key=api_key)
    embedding = client.embeddings.create(
        model=constants.TEXT_EMBEDDING_MODEL,
        input=content,
    )
    return embedding.data[0].embedding


def search(query: str):
    # クライアントを初期化する
    client = QdrantClient("localhost", port=6333)

    # ベクトル化
    query_vector = embedding(query)

    # クエリを実行する
    # 近いベクトルを1つ検索する。
    search_result = client.search(
        collection_name=qdrant_collection,
        query_vector=query_vector,
        limit=search_limit_n,
    )

    return search_result
