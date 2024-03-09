# learn-qdrant
Qdrant の学習用。

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=769590506&skip_quickstart=true)

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
