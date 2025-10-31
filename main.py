from agno.team import Team
from agno.models.azure.openai_chat import AzureOpenAI
from agno.os import AgentOS

from dotenv import load_dotenv
import os

from utils.sqlite_memory import sqlite_db
from utils.logger import get_logger
from utils.mlflow_tracer import setup_mlflow_tracer
from utils.config import (
    MLFLOW_TRACING,
    MLFLOW_TRACK_SERVER,
    MLFLOW_EXPERIMENT_NAME,
    DATABRICKS_HOST,
)

from agents.data_agent import create_agent as create_data_agent
from teams.research_team import create_team

# Load environment variables from .env file
load_dotenv()

# Get logger
logger = get_logger()

# Set up MLflow tracer if enabled
if MLFLOW_TRACING == 'true':
    setup_mlflow_tracer(
        track_server=MLFLOW_TRACK_SERVER,
        experiment_name=MLFLOW_EXPERIMENT_NAME
                            )
    if MLFLOW_TRACK_SERVER == "databricks":
        logger.info(f"Initialized mlflow trace to Databricks: {DATABRICKS_HOST}")
    else:
        logger.info("Initialized mlflow trace to http://localhost:5000")

# Create the Agents

data_agent = create_data_agent()

# Create a team
research_team = create_team(
    member_list=[
                data_agent,
                analyst_agent,
                ]
    )

# Set NO_PROXY to avoid proxy for localhost connections (important for local MCP server access)
os.environ["NO_PROXY"] = "localhost, 127.0.0.1"
os.environ["no_proxy"] = "localhost, 127.0.0.1"

# Create the AgentOS
agent_os = AgentOS(                    
    teams=[research_team],
                    )
# Get the FastAPI app for the AgentOS
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="main:app", port=7777)