# Equivalent Makefile for the MCP project
# Variables
PY := uv run
MLFLOW_UI_PORT := 5000
UI_HOST := 127.0.0.1

# Help command
.PHONY: help
help:
	@echo "Agno OS - Basketball Intelligence"
	@echo ""
	@echo "Available targets:"
	@echo "  start-agno  - Start Agno OS (Multi-agent system connected with MCP Server)"
	@echo "  start-agno-ui - Start AG-UI that interacts with Agno OS"
	@echo "  start-bundle - Start both Agno OS and AG-UI"
	@echo "  start-mlflow  - Start mlflow UI for Agent tracking"
	@echo ""

# Start the AG-UI for Agno OS
.PHONY: start-agno-ui
start-agno-ui:
	cd %USERPROFILE%/agent-ui && npm run dev

# Start Agno OS
.PHONY: start-agno
start-agno:
	$(PY) src/main.py

# Start both Agno OS and AG-UI (AG-UI in the background)
.PHONY: start-bundle
start-bundle:
	$(MAKE) -j2 start-agno start-agno-ui

# Start mlflow UI for Agent tracking
.PHONY: start-mlflow
start-mlflow:
	$(PY) mlflow ui --backend-store-uri sqlite:///mlflow.db --port $(MLFLOW_UI_PORT) --host $(UI_HOST)

# Default target
.DEFAULT_GOAL := help