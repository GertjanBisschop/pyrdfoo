.PHONY: help check lint test-all docs clean format-diff

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

check: ## Run static type checking on the Python code
	@uv run pyright

lint: ## Run linting on the Python code
	@uv run ruff check

test-all: ## Run repository tests
	@uv run pytest

docs: ## Build the documentation
	@uv run sphinx-build -E -a -b html ./docs/source ./docs/build/html

clean: ## Clean documentation artifacts
	-rm -r ./docs/source/modules
	-rm -r ./docs/build

format-diff:
	@uv run --group dev ruff format . --diff