import asyncio

import os
import sys
# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
import mlflow
from mlflow.entities import SpanType
from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.website_reader import WebsiteReader
from agno.vectordb.qdrant import Qdrant

from utils.config import (
    get_llm_config, 
    sqlite_db, 
    llm_catalog, 
    Qdrant_URL,
    MLFLOW_TRACING,
    MLFLOW_TRACK_SERVER,
    MLFLOW_EXPERIMENT_NAME,
    DATABRICKS_HOST,
)
from utils.knowledge_base import create_knowledge_base
from utils.mlflow_tracer import setup_mlflow_tracer
from utils.logger import get_logger

logger = get_logger()

# Set NO_PROXY to avoid proxy for localhost connections
os.environ["NO_PROXY"] = "localhost, 127.0.0.1"
os.environ["no_proxy"] = "localhost, 127.0.0.1"

# Create knowledge base
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

@mlflow.trace(span_type=SpanType.AGENT)
def get_agent():
    return Agent(
                model=get_llm_config(
                'OpenAI-mini',
                llm_catalog.get("OpenAI-mini", "gpt-4.1-mini")
                ),
                knowledge=knowledge_base
                )

if __name__ == "__main__":

    # Load knowledge base asynchronously
    asyncio.run(knowledge_base.add_content_async(
            url="https://www.nba.com/stats/help/glossary",
            skip_if_exists=True
        )
    )

    asyncio.run(get_agent().aprint_response("What does the advanced stats TS% mean?", markdown=True))
