.PHONY: help setup test dev api graph schema clean

VENV := .venv
PY   := $(VENV)/bin/python
PIP  := $(VENV)/bin/pip

help:
	@grep -E '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

setup: ## Create the venv and install the agent stack
	python3 -m venv $(VENV)
	$(PIP) install -q --upgrade pip
	$(PIP) install -q -r agent/requirements.txt pytest httpx
	@test -f .env || cp .env.example .env
	@echo "ready — fill in .env"

test: ## Run the smoke tests (no API key needed)
	cd agent && ../$(PY) -m pytest -q

api: ## Serve the agent on :8000
	cd agent && ../$(PY) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

graph: ## Open the LangGraph dev UI (graph inspector + time travel)
	cd agent && ../$(VENV)/bin/langgraph dev

clean:
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
	rm -rf .pytest_cache agent/.pytest_cache agent/.langgraph_api
