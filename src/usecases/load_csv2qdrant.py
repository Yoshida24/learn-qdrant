"""
埋め込みベクトル付きcsvデータをQdrantにinsertするプログラムです。

ロードできるcsvの形式:
以下の属性を含む
- （必須）idとして使う属性(collection内で一意)
- （必須）埋め込みベクトルの属性("[-0.007615094, 0.013458884]" の形式)
- （任意）メタデータとして埋め込みたい属性

サンプルcsvデータ:
```
data_use_as_id,foo,bar,embeddings_text
https://example.com/unique/string,content title,content body,"[-0.007615094, 0.013458884]"
```
"""

import pandas as pd
from dataclasses import dataclass, asdict

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.models import PointStruct

from typing import Any
embeddings_attr = "embeddings_text"


@dataclass
class QdrantPayload:
    id: int | str
    vector: list[float]
    payload: dict[str, Any]


# ユーザー定義の変数
csv_file_path = "src/dataset/dir/foo.csv"
qdrant_collection = "foo-dev-0-2-0"


# CSVデータを読み込む
def csv_to_list(file_path: str):
    df = pd.read_csv(file_path)
    datam = [row.to_dict() for index, row in df.iterrows()]
    return datam


# embeddingしたデータを作成する
def create_qdrant_payload(rows: list[dict]):
    qdrant_payloads: list = []
    for i, row in enumerate(rows):
        try:
            embeddings_text: list[float] = [
                float(num)
                for num in row[embeddings_attr]
                .strip("[")
                .strip("]")
                .strip(" ")
                .split(",")
            ]
            # 全部3072次元かを調べる
            if len(embeddings_text) != 3072:
                raise Exception("{i} is not 3072 dimension")

            # Extract attributes other than embeddings_text from the csv and convert them to a dictionary array, parsing the values as strings
            qdrant_payloads.append(
                QdrantPayload(
                    id=i,
                    vector=embeddings_text,
                    payload={
                        attr: str(row[attr]) if attr in row and row[attr] != "" else ""
                        for attr in row.keys()
                        if attr != embeddings_attr
                    },
                )
            )
            import time
        except Exception as e:
            continue

        time.sleep(0)
    return qdrant_payloads


# Qdrantにembeddingしたデータを登録する
def register_embedding(qdrant_payloads: list[QdrantPayload]):
    # クライアントを初期化する
    client = QdrantClient("localhost", port=6333)

    # コレクションを作成する
    client.create_collection(
        collection_name=qdrant_collection,
        vectors_config=VectorParams(size=3072, distance=Distance.DOT),
    )

    # ベクトルを追加する
    batch_size = 100
    for i in range(1, len(qdrant_payloads), batch_size):
        batch_payloads = qdrant_payloads[i : i + batch_size]
        operation_info = client.upsert(
            collection_name=qdrant_collection,
            wait=True,
            points=[
                PointStruct(**asdict(qdrant_payload))
                for qdrant_payload in batch_payloads
            ],
        )
        print(f"batch: {i}")

    return operation_info


# メイン関数
def main():
    # CSVデータを読み込む
    articles = csv_to_list(csv_file_path)

    # Qdrantにembeddingしたデータを作成する
    qdrant_payloads = create_qdrant_payload(articles)

    # Qdrantにembeddingしたデータを登録する
    operation_info = register_embedding(qdrant_payloads)

    print("Data registration complete.")


if __name__ == "__main__":
    main()
