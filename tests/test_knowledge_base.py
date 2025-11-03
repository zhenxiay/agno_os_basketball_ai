import asyncio

import os
import sys
# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.website_reader import WebsiteReader
from agno.vectordb.qdrant import Qdrant

from utils.config import (
    get_llm_config, 
    sqlite_db, 
    llm_catalog, 
    Qdrant_URL,
)
from utils.knowledge_base import create_knowledge_base

# Set NO_PROXY to avoid proxy for localhost connections
os.environ["NO_PROXY"] = "localhost, 127.0.0.1"
os.environ["no_proxy"] = "localhost, 127.0.0.1"

# Create knowledge base
knowledge_base = create_knowledge_base(COLLECTION_NAME="thai_recipe_knowledge")

agent = Agent(
    model=get_llm_config('OpenAI-mini',llm_catalog.get("OpenAI-mini", "gpt-4.1-mini")),
    knowledge=knowledge_base
    )

if __name__ == "__main__":

    # Load knowledge base asynchronously
    asyncio.run(knowledge_base.add_content_async(
            url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
            skip_if_exists=True
        )
    )

    asyncio.run(agent.aprint_response("What does the advanced stats %3PA mean?", markdown=True))
