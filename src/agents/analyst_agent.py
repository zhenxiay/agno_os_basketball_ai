'''
This module defines an analyst agent based on pandas dataframe.
'''
from textwrap import dedent
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union, cast

from agno.tools.pandas import PandasTools
from agno.knowledge.knowledge import Knowledge
from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools

from utils.agent_instructions import get_analyst_agent_instructions
from utils.logger import get_logger
from utils.config import (
    get_llm_config,
    sqlite_db,
    llm_catalog,
    )

# Initialize logger
logger = get_logger()

def create_agent(
        llm: str, 
        llm_reasoning: Optional[str],
        knowledge_base: Knowledge) -> Agent:
    '''
    This function creates an agent as basketball analyst.

    Args:
        llm: The LLM model to use for the team ("claude", "OpenAI-mini","OpenAI" or "AzureOpenAI")
        llm_reasoning: The LLM model for reasoning ("claude", "OpenAI-mini", "OpenAI" or "AzureOpenAI")
        model_id: The model ID to use for the LLM. Options: "claude-sonnet-4-5", "gpt-4.1-mini", "gpt-4.1"
        knowledge_base: The knowledge base to be used by the agent
    '''

    agent = Agent(
        name="Basketball Analyst Agent",
        model=get_llm_config(
                    provider=llm,
                    model_id=llm_catalog.get(llm)
                    ),
        reasoning_model=get_llm_config(
                    provider=llm_reasoning,
                    model_id=llm_catalog.get(llm_reasoning, llm)
                    ),
        db=sqlite_db(),
        tools=[
            PandasTools(),
            ReasoningTools(add_instructions=True),
            ],
        instructions=get_analyst_agent_instructions(),
        knowledge=knowledge_base,
        search_knowledge=True,
        add_history_to_context=True,
        enable_user_memories=True,
        markdown=True,
    )
    
    return agent
