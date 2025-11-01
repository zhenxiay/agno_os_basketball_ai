'''
This module defines an agent configured to interact with a MS SQL Server instance via MCPTools.
'''
from textwrap import dedent
from agno.tools import tool
from agno.tools.pandas import PandasTools
from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools

from BasketIntelligence.create_season import CreateSeason
from BasketIntelligence.ml_analysis import k_means_team_shooting_clustering

from utils.agent_instructions import (
    get_data_agent_instructions,
    get_data_agent_output,
    )
from utils.logger import get_logger
from utils.config import (
    get_llm_config,
    sqlite_db,
    )

# Initialize logger
logger = get_logger()

@tool(stop_after_tool_call=True)
def get_team_shooting_data(season: str):
    """
    Get the team shooting data for a given season.
    This data can be combined to generate clustering analysis    
    """
    dataset = CreateSeason(season).read_team_shooting()
    return dataset.to_markdown()

@tool(stop_after_tool_call=True)
def get_team_shooting_clustering(season: str, n_cluster: int):
    """Get the team shooting clustering data for a given season."""

    return k_means_team_shooting_clustering(season, n_cluster).to_markdown()

def create_agent(llm: str = "claude") -> Agent:
    '''
    This function creates an agent as basketball analyst.

    Args:
        llm: The LLM model to use ("claude" or "AzureOpenAI")
    '''

    agent = Agent(
        name="Basketball Analyst Agent",
        model=get_llm_config(llm),
        reasoning_model=get_llm_config(llm),
        db=sqlite_db(),
        tools=[
            get_team_shooting_data,
            get_team_shooting_clustering,
            PandasTools(),
            ReasoningTools(add_instructions=True),
            ],
        instructions=get_data_agent_instructions(),
        expected_output=dedent(get_data_agent_output),
        add_history_to_context=True,
        enable_user_memories=True,
        markdown=True,
    )

    return agent
