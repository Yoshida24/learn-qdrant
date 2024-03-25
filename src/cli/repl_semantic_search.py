from src.usecases.search import search


def main():
    print("\n=== 🤖セマンティック検索を開始します。 ===\n")
    query = input(
        "検索ワードを入力してください。 (例:「チャットボット メモリ管理」「データ タグ 分類」「データベース 連携」)\n\n🔍 検索ワード: "
    )
    while True:
        response = search(query)
        print(
            f"""
あなたの検索ワード:
    - {query}
"""
        )

        print(
            f"""✅ 検索結果:
"""
        )
        for i, article in enumerate(response):
            print(
                f"""    - {i}th:
        - 記事タイトル: {article.payload["title"]}
        - 記事URL: {article.payload["url"]}
        - 類似度スコア(dot product): {article.score}
        - 記事ID: {article.id}
        - バージョン: {article.version}
"""
            )
        query = input(
            "\nお探しの結果は見つかりましたか？\n\nもう一度検索する場合、検索ワードを入力してください:\n\n🔍 検索ワード:"
        )


main()
