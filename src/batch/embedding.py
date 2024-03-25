import os
import glob
import pandas as pd
import re
from openai import OpenAI
import src.constants as constants
from dataclasses import dataclass, asdict

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.models import PointStruct

from typing import Any


# ユーザー定義の変数
root_in_target_docs_dir = "langchain"
qdrant_collection = "langchain-docs-semanticsearch-dev-0-2-0"


@dataclass
class Article:
    path: str
    file: str
    content: str


@dataclass
class DocsMetadata:
    title: str
    url: str
    content: str


@dataclass
class QdrantPayload:
    id: int
    vector: list[float]
    payload: dict[str, Any]


def load_files() -> dict[str, list[Article]]:
    """_summary_
    Example:

    ```python
    [
        {
            "path": "/docs/use_cases/apis",
            "file": apis,
            "content": "{\n "cells": [\n  {\n   "cell_type": "raw",\n ...",
        }
    ]
    ```

    Args:
        _no_args_
    Returns:
        dict[str, list[str]]: _description_
    """

    # Step 1: Get all files recursively
    files = glob.glob(target_docs_dir, recursive=True)

    # Step 2, 3 & 4: Extract path, file name and content
    articles = []
    for file in files:
        print(file)
        if os.path.isfile(file):
            parts = file.split("/")
            use_cases_index = parts.index(root_in_target_docs_dir)
            path_with_extention = "/" + "/".join(parts[use_cases_index + 1 :])
            path = re.sub(r"\.(.*)$", "", path_with_extention)
            file_name, _ = os.path.splitext(parts[-1])
            print(file_name)
            with open(
                file, "r"
            ) as f:  # Use the original 'file' variable with extension
                content = f.read()
            articles.append(Article(path, file_name, content))

    # Step 5: Sort and create dictionary
    articles = sorted(articles, key=lambda x: x.path)
    result = {"articles": articles}
    return result


# content -> embedding
def embedding(content: str) -> list[float]:
    api_key = os.getenv(constants.ENV_OPENAI_API_KEY)
    client = OpenAI(api_key=api_key)
    embedding = client.embeddings.create(
        model=constants.TEXT_EMBEDDING_MODEL,
        input=content,
    )
    return embedding.data[0].embedding


# embeddingしたデータを作成する
def create_qdrant_payload(articles: list[Article]):
    qdrant_payloads: list[QdrantPayload] = []
    for i, article in enumerate(articles):
        content_in_max_token = (
            article.content
            if len(article.content) <= constants.MAX_TOKEN_IN_TEXT_EMBEDDING_3_SMALL
            else article.content[: constants.MAX_TOKEN_IN_TEXT_EMBEDDING_3_SMALL]
        )
        embedded_content = embedding(content_in_max_token)
        url = f"https://python.langchain.com{article.path}"
        qdrant_payloads.append(
            QdrantPayload(
                id=i,
                vector=embedded_content,
                payload={
                    "title": article.file,
                    "url": url,
                    "content": article.content,
                },
            )
        )
        print(f"embedded {i}th article")
        import time

        time.sleep(1)
    return qdrant_payloads


# Qdrantにembeddingしたデータを登録する
def register_embedding(qdrant_payloads: list[QdrantPayload]):
    # クライアントを初期化する
    client = QdrantClient("localhost", port=6333)

    # コレクションを作成する
    client.create_collection(
        collection_name=qdrant_collection,
        vectors_config=VectorParams(
            size=constants.DIMENSION_IN_TEXT_EMBEDDING_3_SMALL, distance=Distance.DOT
        ),
    )

    # ベクトルを追加する
    for qdrant_payload in qdrant_payloads:
        operation_info = client.upsert(
            collection_name=qdrant_collection,
            wait=True,
            points=[
                PointStruct(**asdict(qdrant_payload))
                for qdrant_payload in qdrant_payloads
            ],
        )

    return operation_info


def main():
    files = load_files()
    articles = files["articles"]
    print(pd.DataFrame(articles))

    qdrant_payloads = create_qdrant_payload(articles)
    print(pd.DataFrame(qdrant_payloads).head(5))
    print("embedding dimension: " + str(len(qdrant_payloads[0].vector)))

    operation_info = register_embedding(qdrant_payloads)
    print(operation_info)


main()
