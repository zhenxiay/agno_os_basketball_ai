'''
This module defines an agent configured to interact with a MS SQL Server instance via MCPTools.
'''
from textwrap import dedent
import pandas_toon
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union, cast
from pathlib import Path

from agno.tools import tool
from agno.agent import Agent
from agno.skills import Skills, LocalSkills

from utils.logger import get_logger
from utils.config import (
    get_llm_config,
    sqlite_db,
    llm_catalog,
    )

# Initialize logger
logger = get_logger()

# Get skills directory relative to this file
skills_dir = Path(__file__).parent.parent.parent / ".github" / "skills"

def create_agent(llm: str) -> Agent:
    '''
    This function creates an agent as basketball analyst.

    Args:
        llm: The LLM model to use for the team ("claude", "OpenAI-mini","OpenAI" or "AzureOpenAI")
        model_id: The model ID to use for the LLM. Options: "claude-sonnet-4-5", "gpt-4.1-mini", "gpt-4.1"
    '''

    agent = Agent(
        name="Basketball Game Report Agent",
        model=get_llm_config(
                    provider=llm,
                    model_id=llm_catalog.get(llm)
                    ),
        db=sqlite_db(),
        skills=Skills(loaders=[LocalSkills(str(skills_dir))]),
        instructions=[
        "You are a helpful assistant with access to specialized skills."
        ],
        add_history_to_context=True,
        enable_user_memories=True,
        markdown=True,
    )

    return agent