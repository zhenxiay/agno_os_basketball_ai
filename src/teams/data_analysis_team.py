'''
This module defines a data analysis team for basketball statistics.
'''
from agno.team import Team
from agno.models.azure.openai_chat import AzureOpenAI
from agno.tools.reasoning import ReasoningTools

from utils.config import (
    get_llm_config,
    sqlite_db,
    )
from utils.agent_instructions import get_team_instructions

def create_team(member_list: list, llm: str) -> Team:
    '''
    Create a data analysis team with the given members.

    Args:
        member_list: List of Agent instances to be members of the team.
        llm: The LLM model to use for the team ("claude", "OpenAI" or "AzureOpenAI")

    Returns:
        An instance of Team configured as a data analysis team.
    '''
    analyst_team = Team(
        name="Data Analysis Team",
        description="A team of agents that collaborates to analyze basketball data.",
        members=member_list,
        model=get_llm_config(llm),
        id="data_analysis_team",
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            get_team_instructions(),
        ],
        db=sqlite_db(),
        share_member_interactions=True,
        add_team_history_to_members=True,
        enable_user_memories=True,
        add_history_to_context=True,
        add_datetime_to_context=True,
        markdown=True,
    )

    return analyst_team
