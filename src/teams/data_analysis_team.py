'''
This module defines a data analysis team for basketball statistics.
'''
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union, cast

from agno.team import Team
from agno.models.azure.openai_chat import AzureOpenAI
from agno.tools.reasoning import ReasoningTools
from agno.knowledge.knowledge import Knowledge

from utils.config import (
    get_llm_config,
    sqlite_db,
    llm_catalog,
    )
from utils.agent_instructions import get_team_instructions

def create_team(
        member_list: list, 
        llm: str, 
        llm_reasoning: Optional[str],
        knowledge_base: Knowledge,
        ) -> Team:
    '''
    Create a data analysis team with the given members.

    Args:
        member_list: List of Agent instances to be members of the team.
        llm: The LLM model to use for the team ("claude", "OpenAI" or "AzureOpenAI")
        model_id: The model ID to use for the LLM. Options: "claude-sonnet-4-5", "gpt-4.1-mini", "gpt-4.1"

    Returns:
        An instance of Team configured as a data analysis team.
    '''
    analyst_team = Team(
        name="Data Analysis Team",
        description="A team of agents that collaborates to analyze basketball data.",
        members=member_list,
        model=get_llm_config(
                    provider=llm,
                    model_id=llm_catalog.get(llm)
                    ),
        reasoning_model=get_llm_config(
                    provider=llm_reasoning,
                    model_id=llm_catalog.get(llm_reasoning, llm),
                    ),
        id="data_analysis_team",
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            get_team_instructions(),
        ],
        knowledge=knowledge_base,
        db=sqlite_db(),
        share_member_interactions=True,
        add_team_history_to_members=True,
        enable_user_memories=True,
        add_history_to_context=True,
        add_datetime_to_context=True,
        markdown=True,
    )

    return analyst_team
