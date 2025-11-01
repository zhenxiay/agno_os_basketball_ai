import asyncio

import os
import sys
# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.qdrant import Qdrant

from utils.config import get_llm_config

COLLECTION_NAME = "thai-recipes"

# Initialize Qdrant with local instance
vector_db = Qdrant(
    collection=COLLECTION_NAME, 
    url="http://localhost:6666"
)

# Create knowledge base
knowledge_base = Knowledge(
    vector_db=vector_db,
)

agent = Agent(
    model=get_llm_config('OpenAI'),
    knowledge=knowledge_base
    )

if __name__ == "__main__":
    # Load knowledge base asynchronously
    asyncio.run(knowledge_base.add_content_async(
            url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
        )
    )

    asyncio.run(agent.aprint_response("How to make Tom Kha Gai", markdown=True))