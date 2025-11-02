'''
This module defines an analyst agent based on pandas dataframe.
'''
from textwrap import dedent
from agno.tools.pandas import PandasTools
from agno.knowledge.knowledge import Knowledge
from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools

from utils.agent_instructions import get_analyst_agent_instructions
from utils.logger import get_logger
from utils.config import (
    get_llm_config,
    sqlite_db,
    )

# Initialize logger
logger = get_logger()

def create_agent(llm: str, 
                 knowledge_base: Knowledge) -> Agent:
    '''
    This function creates an agent as basketball analyst.

    Args:
        llm: The LLM model to use for the team ("claude", "OpenAI" or "AzureOpenAI")
        model_id: The model ID to use for the LLM. Options: "claude-sonnet-4-5", "gpt-4.1-mini", "gpt-4.1"
        knowledge_base: The knowledge base to be used by the agent
    '''

    agent = Agent(
        name="Basketball Analyst Agent",
        model=get_llm_config(llm,"gpt-4.1"),
        reasoning_model=get_llm_config(llm, "gpt-4.1-mini"),
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
