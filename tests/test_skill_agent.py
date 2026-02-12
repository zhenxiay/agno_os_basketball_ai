'''
This module tests whether the agent with agent skills is configured correctly.
'''
import os
import sys
from dotenv import load_dotenv

# Add src to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from agno.os import AgentOS
from agents.game_report_agent import create_agent as create_game_report_agent

from utils.logger import get_logger

logger = get_logger()

# Load environment variables from .env file
load_dotenv()

# Set NO_PROXY to avoid proxy for localhost connections (important for local MCP server access)
os.environ["NO_PROXY"] = "localhost, 127.0.0.1"
os.environ["no_proxy"] = "localhost, 127.0.0.1"

def create_test_agent():
    '''
    Test function for Game Report Agent.
    '''
    try:
        agent = create_game_report_agent(
                llm="OpenAI", 
                )
        logger.info(agent.name)
    except Exception as e:
        logger.error(f"Error while testing Game Report Agent: {e}")

    return agent

if __name__ == "__main__":
    agent = create_test_agent()
    agent.print_response("Create a report for the game between HOU and ORL on 2025-11-16.")