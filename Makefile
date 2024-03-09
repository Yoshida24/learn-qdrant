.PHONY: search
search:
	@echo "Running..."
	bash scripts/search.sh

.PHONY: seed
seed:
	@echo "Running..."
	bash scripts/seed.sh

.PHONY: setup
setup:
	@echo "Setup..."
	bash scripts/setup.sh

.PHONY: serve
serve:
	@echo "Serving..."
	sh scripts/serve.sh

.PHONY: test
test:
	@echo "Testing..."
	bash scripts/test.sh
