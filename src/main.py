import asyncio
from agno.team import Team
from agno.os import AgentOS
from agno.knowledge.reader.website_reader import WebsiteReader

from dotenv import load_dotenv
import os
from utils.logger import get_logger
from agents.data_agent import create_agent as create_data_agent
from agents.analyst_agent import create_agent as create_analyst_agent
from agents.visual_agent import create_agent as create_visual_agent
from teams.data_analysis_team import create_team as create_data_analysis_team

from utils.knowledge_base import create_knowledge_base

# Get logger
logger = get_logger()

# crate knowledge base
knowledge_base = create_knowledge_base(COLLECTION_NAME="basketball_knowledge")

# Create agents
data_agent = create_data_agent(llm="OpenAI")
analyst_agent = create_analyst_agent(
    llm="OpenAI", 
    knowledge_base=knowledge_base
    )
visual_agent = create_visual_agent(llm="OpenAI")
member_list = [data_agent, analyst_agent, visual_agent]

# Create a team
analysis_team = create_data_analysis_team(
    member_list=member_list, 
    llm="OpenAI"
    )

# Set NO_PROXY to avoid proxy for localhost connections
os.environ["NO_PROXY"] = "localhost, 127.0.0.1"
os.environ["no_proxy"] = "localhost, 127.0.0.1"

# Create the AgentOS
agent_os = AgentOS(                    
    teams=[analysis_team],
                    )
# Get the FastAPI app for the AgentOS
app = agent_os.get_app()

if __name__ == "__main__":

    # Load knowledge base asynchronously
    asyncio.run(knowledge_base.add_content_async(
            url="https://www.nba.com/stats/help/glossary",
            reader=WebsiteReader(max_depth=2, max_links=20),
            skip_if_exists=True
        )
    )
    
    # Serve the AgentOS app
    agent_os.serve(app="main:app", port=7777)
