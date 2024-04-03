#!/bin/bash
set -a && . ./.env && set +a
python src/usecases/load_csv2qdrant.py
