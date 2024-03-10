from qdrant_client import QdrantClient


def search():
    # クライアントを初期化する
    client = QdrantClient("localhost", port=6333)

    # クエリを実行する
    # [0.2, 0.1, 0.9, 0.7] に近いベクトルを3つ検索する。
    search_result = client.search(
        collection_name="test_collection", query_vector=[0.2, 0.1, 0.9, 0.7], limit=3
    )

    print(search_result)


search()
