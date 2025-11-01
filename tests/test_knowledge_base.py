import asyncio

import os
import sys
# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.website_reader import WebsiteReader
from agno.vectordb.qdrant import Qdrant

from utils.config import get_llm_config, sqlite_db

COLLECTION_NAME = "thai-recipes"

# Initialize Sqlite for knowledge contents
contents_db = sqlite_db(
                        db_path="knowledge_base.db"
                        )

# Initialize Qdrant with local instance
vector_db = Qdrant(
    collection=COLLECTION_NAME, 
    url="http://localhost:6666"
)

# Create knowledge base
knowledge_base = Knowledge(
    vector_db=vector_db,
    contents_db=contents_db,
)

agent = Agent(
    model=get_llm_config('OpenAI'),
    knowledge=knowledge_base
    )

if __name__ == "__main__":
    # Load knowledge base asynchronously
    asyncio.run(knowledge_base.add_content_async(
            url="https://www.nba.com/stats/help/glossary",
            reader=WebsiteReader(max_depth=2, max_links=20),
            skip_if_exists=True
        )
    )

    asyncio.run(agent.aprint_response("What does the advanced stats %3PA mean?", markdown=True))
