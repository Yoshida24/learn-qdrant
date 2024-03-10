# learn-qdrant
Qdrant の学習用。

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=686856069&skip_quickstart=true)

## Usage

depends on:
- Python: 3.11.2
- pip: 22.3.1
- GNU Make: 3.81

support:
- OS: M1 Macbook Air Ventura 13.4.1

## Gettig Started
First of all, install VSCode recommended extensions. This includes Linter, Formatter, and so on. Recommendation settings is written on `.vscode/extensions.json`.

Make `venv`:

```
python -m venv .venv && . .venv/bin/activate
```

Install dependeincies:

```
pip install -r requirements.txt
```

Duplicate `.env` :

```
cp .env.sample .env
echo '.env is created. please set env.'
```

Then, install Docker dependencies:

```bash
make setup
```

Serve Qdrant:

```bash
make serve
```

> **Note**
This project *does not* depends on `dotenv-python`. Instead, using below script.
> `set -a && source ./.env && set +a`

## Functions

### Register first Vectors

```bash
make seed
```

### Search similer vector

```bash
make search
```

## Semantic Search
自分で用意したドキュメントをメタデータ付きでQdrantに登録するには、`embedding.py` を参考に実装を行ってください。
このリポジトリにはLangChainのドキュメント74ページ分のサンプルが付属しており、`embedding.py`によってそれをVectorDBに登録するテストを体験することができます。
サンプルデータの登録を行うには、以下のコマンドを実行します。

```bash
python src/semantic_search/embedding.py
```

このサンプルデータに対してセマンティック検索をCLIで行うには、以下を実行してください。

```bash
python src/semantic_search/repl_semantic_search.py
```

以下のように対話的に検索を実行することができます。

```
=== 🤖セマンティック検索を開始します。 ===


検索ワードを入力してください:
🔍 SQL

Your Query:
    - SQL

Search Result:

    - 0th:
        - score: 0.38316363
        - id: 62
        - title: query_checking
        - url: https://python.langchain.com/docs/use_cases/sql/query_checking
        - version: 74

    - 1th:
        - score: 0.37933916
        - id: 58
        - title: agents
        - url: https://python.langchain.com/docs/use_cases/sql/agents
        - version: 74

もう一度検索する場合、検索ワードを入力してください:
🔍
```

CLIではなくコードによって検索を実装したい場合、`search.py`の実装を参考にしてください。

> **Note**
> `repl_semantic_search.py` も内部的には `search.py` を利用しています。


## Develop App
On usual develop, first you activate `venv` first like below.

```bash
source .venv/bin/activate
```

Save requirements:

```bash
pip freeze > requirements.txt
```

Deactivate venv:

```bash
deactivate
```
