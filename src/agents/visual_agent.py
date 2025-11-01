'''
This module defines an analyst agent based on pandas dataframe.
'''
from textwrap import dedent
from agno.tools.visualization import VisualizationTools
from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools

from utils.agent_instructions import get_data_agent_output, get_visualization_agent_instructions
from utils.logger import get_logger
from utils.config import (
    get_llm_config,
    sqlite_db,
    )

# Initialize logger
logger = get_logger()

def create_agent(llm: str) -> Agent:
    '''
    This function creates an agent as basketball analyst.

    Args:
        llm: The LLM model to use for the team ("claude", "OpenAI" or "AzureOpenAI")
    '''

    agent = Agent(
        name="Basketball Visualization Agent",
        model=get_llm_config(llm),
        reasoning_model=get_llm_config(llm),
        db=sqlite_db(),
        tools=[
            VisualizationTools("visuals"),
            ReasoningTools(add_instructions=True),
            ],
        instructions=get_visualization_agent_instructions(),
        add_history_to_context=True,
        enable_user_memories=True,
        markdown=True,
    )
    
    return agent
