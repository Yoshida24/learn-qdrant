# Azure OpenAI Service を使う
import pandas as pd
import requests
import json
from tenacity import (
    retry,
    wait_exponential,
    stop_after_attempt,
    before_sleep_log,
    retry_if_exception_type,
)
import logging
import dotenv
import os

# ユーザー定義の変数
csv_input_path = "src/dataset/path/foo.csv"
csv_output_path = "src/dataset/path/bar.csv"
csv_fail_output_path = "src/dataset/path/bar_fail.csv"
vectorize_column = "text"
head: None | int = None
skip_rows = 0

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Azure OpenAIの設定
dotenv.load_dotenv()
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
API_VERSION = os.getenv("API_VERSION")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")


def get_embeddings(text: str | None, row_index):
    """指定されたテキストに対するembeddingsをAzure OpenAI APIを使って取得"""
    print(f"Processing row {row_index + 1}: {text}")
    endpoint = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{DEPLOYMENT_NAME}/embeddings?api-version={API_VERSION}"
    headers = {"Content-Type": "application/json", "api-key": AZURE_OPENAI_API_KEY}
    if pd.isna(text):
        data = {"input": "nan"}
    else:
        data = {"input": text}

    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        embedding_data = response.json()
        embedding = embedding_data.get("data")[0]["embedding"]
        return embedding
    else:
        response.raise_for_status()


@retry(
    wait=wait_exponential(multiplier=2, max=16),  # 2秒、4秒、8秒、16秒の指数バックオフ
    stop=stop_after_attempt(5),  # 最大5回までリトライ
    before_sleep=before_sleep_log(logger, logging.INFO),  # リトライ前にログを出力
    retry=retry_if_exception_type(requests.HTTPError),
)  # HTTPエラー時のみリトライ
def robust_get_embeddings(text, row_index):
    try:
        return get_embeddings(text, row_index)
    except requests.HTTPError as e:
        print(f"Failed to get embeddings for row {row_index + 1}: {e}")
        raise e


# CSVファイルを読み込む
df = (
    pd.read_csv(csv_input_path)[skip_rows:]
    if head is None
    else pd.read_csv(csv_input_path, skiprows=skip_rows)[skip_rows:head]
)

try:
    # embeddingsを計算し、新しいカラムに追加
    for index, row in df.iterrows():
        try:
            embedding = robust_get_embeddings(row[vectorize_column], index)
            # embeddingベクトルをJSON形式の文字列に変換してDataFrameに設定
            df.at[index, "embeddings_text"] = json.dumps(embedding)
        except Exception as e:
            print({e})
            df[:index].to_csv(csv_fail_output_path, index=False)
            raise Exception(
                f"Process stopped due to failure at row {index}. Partial data saved to {csv_fail_output_path}"
            ) from e

    # 成功した結果をCSVファイルに保存
    df.to_csv(csv_output_path, index=False)
except Exception as e:
    logger.error(e)
