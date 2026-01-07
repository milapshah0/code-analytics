.PHONY: setup start test clean

PYTHON = python3.13
VENV = .venv
BIN = $(VENV)/bin

setup:
	uv sync

start:
	$(BIN)/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	$(BIN)/pytest

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
