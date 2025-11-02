"""
Configuration module for the agent application.
"""

import os
import json
from dotenv import load_dotenv

from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.models.azure.openai_chat import AzureOpenAI
from agno.models.openai.responses import OpenAIResponses

# Load environment variables
load_dotenv()

# Environment variables for mlflow tracer
MLFLOW_TRACING=os.getenv("MLFLOW_TRACING", "false")  # Default to false if not specified
MLFLOW_TRACK_SERVER = os.getenv("MLFLOW_TRACK_SERVER", "local")  # Default to local if not specified
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "MCP_Experiments")  # Default experiment name
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST", "local")

# Qdrant URL configuration for vector database as Knowledge Base
Qdrant_URL = os.getenv("Qdrant_URL", "http://localhost:6333")

# Define function for LLM configuration
def get_llm_config(provider: str, model_id: str):
    """
    Get the LLM configuration based on the provider.

    Args:
        provider: The LLM provider ("claude", "OpenAI" or "AzureOpenAI")
        model_id: The model ID to use for the LLM. Options: "claude-sonnet-4-5", "gpt-4.1-mini", "gpt-4.1".

    Returns:
        An instance of the corresponding LLM model.
    """
    llm = Claude(model_id) if provider == "claude" \
          else OpenAIResponses(id=model_id) if provider == "OpenAI" \
          else AzureOpenAI(id=model_id, api_version="2024-12-01-preview")

    return llm

# Define function for SQLite database configuration as memory store
def sqlite_db(db_path: str = "agno.db") -> SqliteDb:
    '''
    This function configures and returns a SQLite database for use as a memory store.

    Args:
        db_path (str): The file path for the SQLite database. Defaults to "agno.db".

    Returns:
        SqliteDb: An instance of SqliteDb configured with the specified database file.
    '''
    return SqliteDb(db_file=db_path)
