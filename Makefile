.PHONY: start
start:
	@echo "Starting..."
	@echo "open docs: http://127.0.0.1:8000/docs"
	uvicorn src.main:app --reload

.PHONY: setup
setup:
	@echo "Setup..."
	bash scripts/setup.sh

.PHONY: serve
serve:
	@echo "Serving..."
	sh scripts/serve.sh

.PHONY: import_csv
import_csv:
	@echo "Importing csv..."
	sh scripts/import_csv.sh

.PHONY: test
test:
	@echo "Testing..."
	bash scripts/test.sh
