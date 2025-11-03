'''
This module tests whether various agents are configured corrected.
'''
import os
import sys
from dotenv import load_dotenv

# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from agno.os import AgentOS
from agents.analyst_agent import create_agent as create_analyst_agent
from agents.data_agent import create_agent as create_data_agent
from teams.data_analysis_team import create_team as create_data_analysis_team

from utils.logger import get_logger
from utils.knowledge_base import create_knowledge_base

logger = get_logger()

# Load environment variables from .env file
load_dotenv()

# Set NO_PROXY to avoid proxy for localhost connections (important for local MCP server access)
os.environ["NO_PROXY"] = "localhost, 127.0.0.1"
os.environ["no_proxy"] = "localhost, 127.0.0.1"

def test_team():
    '''
    Test function for Data Analysis Team.
    '''
    try:
        analysis_team = create_data_analysis_team(
                member_list=[
                    create_data_agent(
                            llm="OpenAI", 
                            llm_reasoning="OpenAi-mini",
                            ),
                    create_analyst_agent(
                            llm="OpenAI", 
                            #llm_reasoning="OpenAi-mini",
                            knowledge_base=create_knowledge_base(),
                            ),
                            ], 
                llm="OpenAI"
                )
        logger.info(analysis_team.name)
        logger.info(len(analysis_team.members))
        for agent in analysis_team.members:
            logger.info(agent.name)
    except Exception as e:
        logger.error(f"Error while testing Data Analysis Team: {e}")

if __name__ == "__main__":
    test_team()