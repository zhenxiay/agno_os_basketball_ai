'''
Main entry point to start the agent app.
'''
import asyncio
from agno.team import Team
from agno.os import AgentOS
from agno.knowledge.reader.website_reader import WebsiteReader

import os
from agents.data_agent import create_agent as create_data_agent
from agents.analyst_agent import create_agent as create_analyst_agent
from agents.visual_agent import create_agent as create_visual_agent
from teams.data_analysis_team import create_team as create_data_analysis_team

from utils.knowledge_base import create_knowledge_base
from utils.mlflow_tracer import setup_mlflow_tracer
from utils.config import (
    llm, 
    llm_reasoning, 
    MLFLOW_TRACING,
    MLFLOW_TRACK_SERVER,
    MLFLOW_EXPERIMENT_NAME,
    DATABRICKS_HOST,
)
from utils.logger import get_logger

# Get logger
logger = get_logger()

# Set NO_PROXY to avoid proxy for localhost connections
os.environ["NO_PROXY"] = "localhost, 127.0.0.1"
os.environ["no_proxy"] = "localhost, 127.0.0.1"

# crate knowledge base
knowledge_base = create_knowledge_base(COLLECTION_NAME="basketball_knowledge")

# Set up mlflow tracer
if MLFLOW_TRACING == 'true':
    setup_mlflow_tracer(
        track_server=MLFLOW_TRACK_SERVER,
        experiment_name=MLFLOW_EXPERIMENT_NAME
                        )
    if MLFLOW_TRACK_SERVER == "databricks":
        logger.info(f"Initialized mlflow trace to Databricks: {DATABRICKS_HOST}")
    else:
        logger.info("Initialized mlflow trace to http://localhost:5000")

# Create agents
data_agent = create_data_agent(
    llm, 
    llm_reasoning,
    )
analyst_agent = create_analyst_agent(
    llm,
    llm_reasoning, 
    knowledge_base,
    )
visual_agent = create_visual_agent(
    llm, 
    llm_reasoning,
    )
member_list = [data_agent, analyst_agent, visual_agent]

# Create a team
analysis_team = create_data_analysis_team(
    member_list, 
    llm, 
    llm_reasoning,
    knowledge_base,
    )

# Create the AgentOS
agent_os = AgentOS(                    
    teams=[analysis_team],
    enable_mcp_server=True,
                    )
# Get the FastAPI app for the AgentOS
app = agent_os.get_app()

if __name__ == "__main__":

    # Load knowledge base asynchronously
    asyncio.run(knowledge_base.add_content_async(
            url="https://www.nba.com/stats/help/glossary",
            reader=WebsiteReader(max_depth=2, max_links=5),
            skip_if_exists=True
        )
    )
    
    # Serve the AgentOS app
    agent_os.serve(app="main:app", port=7777)
