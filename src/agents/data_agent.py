'''
This module defines an agent configured to interact with a MS SQL Server instance via MCPTools.
'''
from textwrap import dedent
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union, cast

from agno.tools import tool
from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools

from BasketIntelligence.create_season import CreateSeason
from BasketIntelligence.ml_analysis import (
    k_means_team_shooting_clustering,
    k_means_player_clustering,
    )

from utils.agent_instructions import (
    get_data_agent_instructions,
    get_data_agent_output,
    )
from utils.logger import get_logger
from utils.config import (
    get_llm_config,
    sqlite_db,
    llm_catalog,
    )

# Initialize logger
logger = get_logger()

@tool(
    name="get_team_shooting_clustering",
    description="Get the team clustering data with shooting stats for a given season",
    stop_after_tool_call=False
    )
def get_team_shooting_clustering(
        season: str, 
        n_cluster: Optional[int]= 5
        ):
    """Get the team shooting clustering data for a given season."""
    
    df_shooting = CreateSeason(season).read_team_shooting()
    df_clustering = k_means_team_shooting_clustering(season, n_cluster)
    df_output = df_shooting.join(df_clustering.set_index('Team'), on='Team')

    return df_output

@tool(
    name="get_player_adv_stats_clustering",
    description="Get the player clustering data with advanced stats for a given season",
    stop_after_tool_call=False
    )                                 
def get_player_clustering(
        season: str, 
        n_cluster: Optional[int]= 5
        ):
    """Get the player clustering data with advanced stats for a given season."""
    
    df_adv_stats = CreateSeason(season).read_adv_stats()
    df_clustering = k_means_player_clustering(season, n_cluster)
    df_output = df_adv_stats.merge(df_clustering, on='Player', how='inner')

    return df_output

def create_agent(llm: str, llm_reasoning: Optional[str]) -> Agent:
    '''
    This function creates an agent as basketball analyst.

    Args:
        llm: The LLM model to use for the team ("claude", "OpenAI-mini","OpenAI" or "AzureOpenAI")
        llm_reasoning: The LLM model for reasoning ("claude", "OpenAI-mini", "OpenAI" or "AzureOpenAI")
        model_id: The model ID to use for the LLM. Options: "claude-sonnet-4-5", "gpt-4.1-mini", "gpt-4.1"
        knowledge_base: The knowledge base to be used by the agent
    '''

    agent = Agent(
        name="Basketball Data Agent",
        model=get_llm_config(
                    provider=llm,
                    model_id=llm_catalog.get(llm)
                    ),
        reasoning_model=get_llm_config(
                    provider=llm_reasoning,
                    model_id=llm_catalog.get(llm_reasoning, llm),
                    ),
        db=sqlite_db(),
        tools=[
            get_team_shooting_clustering,
            get_player_clustering,
            ReasoningTools(add_instructions=True),
            ],
        instructions=get_data_agent_instructions(),
        expected_output=dedent(get_data_agent_output()),
        add_history_to_context=True,
        enable_user_memories=True,
        markdown=True,
    )

    return agent
