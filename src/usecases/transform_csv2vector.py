import pandas as pd
import requests
import json
from tenacity import retry, wait_fixed, stop_after_attempt, before_sleep_log
import logging
import dotenv
import os
import time

# ユーザー定義の変数
csv_input_path = "src/dataset/workato/messages.csv"
csv_output_path = "src/dataset/workato/message_with_embeddings.csv"
vectorize_column = "text"

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Azure OpenAIの設定
dotenv.load_dotenv()
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
API_VERSION = os.getenv("API_VERSION")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")


@retry(
    wait=wait_fixed(1)
    + wait_fixed(2)
    + wait_fixed(4)
    + wait_fixed(8)
    + wait_fixed(16),  # exponential wait
    stop=stop_after_attempt(5),  # maximum 5 attempts
    before_sleep=before_sleep_log(logger, logging.INFO),
)  # log before each retry
def get_embeddings(text):
    """指定されたテキストに対するembeddingsをAzure OpenAI APIを使って取得"""
    print(text)
    endpoint = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{DEPLOYMENT_NAME}/embeddings?api-version={API_VERSION}"
    headers = {"Content-Type": "application/json", "api-key": AZURE_OPENAI_API_KEY}
    data = {"input": text}
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        embedding_data = response.json()
        embedding = embedding_data.get("data")[0]["embedding"]
        return embedding
    else:
        response.raise_for_status()  # ステータスコードが200以外の場合は例外を発生


# CSVファイルを読み込む
# df = pd.read_csv(csv_input_path)
df = pd.read_csv(csv_input_path).head(1)  # テスト用に1行だけ読み込む

# embeddingsを計算し、新しいカラムに追加
df["embeddings_text"] = df[vectorize_column].apply(lambda x: get_embeddings(x))

# 結果を新しいCSVファイルに保存
try:
    df.to_csv(csv_output_path, index=False)
except Exception as e:
    print(f"Failed to save the CSV file: {e}")
