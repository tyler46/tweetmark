.PHONY: help clean clean-pyc clean-test
.DEFAULT_GOAL := help

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Python package Tasks
clean: clean-pyc clean-test ## Remove python artifacts

clean-pyc: ## Remove python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '*.sql' -exec rm -f {} +

clean-test: ## Remove test artifacts
	rm -fr .pytest_cache
