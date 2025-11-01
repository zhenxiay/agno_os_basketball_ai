from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.qdrant import Qdrant

from utils.config import (
    get_llm_config, 
    sqlite_db, 
    Qdrant_URL
    )

def create_knowledge_base(COLLECTION_NAME: str = "basketball_knowledge") -> Knowledge:
    '''
    This function creates a knowledge base for the agent.

    Returns:
        knowledge_base: The created knowledge base.

    Args:
        COLLECTION_NAME: The name of the collection in the vector database.
    '''

    # Initialize Sqlite for knowledge contents
    contents_db = sqlite_db(
                        db_path="knowledge_base.db"
                        )

    # Initialize Qdrant with local instance
    vector_db = Qdrant(
        collection=COLLECTION_NAME, 
        url=Qdrant_URL
    )

    # Create knowledge base
    knowledge_base = Knowledge(
        vector_db=vector_db,
        contents_db=contents_db,
    )

    return knowledge_base
